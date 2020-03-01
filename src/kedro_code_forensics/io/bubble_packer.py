import json
import os
from json import JSONDecoder, JSONEncoder
from pathlib import PurePath
from typing import Any, Dict, List, NamedTuple, Optional

from kedro.contrib.io import DefaultArgumentsMixIn
from kedro.io import AbstractVersionedDataSet, Version
from numpy.core import int64

from kedro_code_forensics.io.expections import WriteOnlyDataSet

html_template = """
<html>
    <head>
        <title>Bubble Packer</title>
        <script src="https://d3js.org/d3.v5.min.js"></script>
    </head>
    <body>
        <div id="root"></div>
        <script>
            let color = d3.scaleLinear()
                .domain([0, %(max_domain)s])
                .range(["hsl(183,100%%,71%%)", "hsl(204,90%%,53%%)"])
                .interpolate(d3.interpolateHcl);
            let heat_color = d3.scaleLinear()
                .domain([0, %(max_heat)s])
                .range(["hsl(54,80%%,80%%)", "hsl(360,100%%,30%%)"])
                .interpolate(d3.interpolateHcl);
            let format = d3.format(",d");
            let height = %(height)s;
            let width = %(width)s;
            let data = JSON.parse('%(json)s');
            let pack = data => d3.pack()
                .size([width, height])
                .padding(3)
              (d3.hierarchy(data)
                .sum(d => d.value)
                .sort((a, b) => b.value - a.value))
            const root = pack(data);
            let focus = root;
            let view;

            const svg = d3.select("#root").append("svg")
                .attr("viewBox", `-${width / 2} -${height / 2} ${width} ${height}`)
                .style("display", "block")
                .style("margin", "0 -14px")
                .style("background", color(0))
                .style("cursor", "pointer")
                .on("click", () => zoom(root));

            const node = svg.append("g")
              .selectAll("circle")
              .data(root.descendants().slice(1))
              .join("circle")
                .attr("fill", d => d.children ? color(d.depth) : heat_color(d.value))
                .attr("pointer-events", d => !d.children ? "none" : null)
                .on("mouseover", function() { d3.select(this).attr("stroke", "#000"); })
                .on("mouseout", function() { d3.select(this).attr("stroke", null); })
                .on("click", d => focus !== d && (zoom(d), d3.event.stopPropagation()));

            const label = svg.append("g")
                .style("font", "10px sans-serif")
                .attr("pointer-events", "none")
                .attr("text-anchor", "middle")
              .selectAll("text")
              .data(root.descendants())
              .join("text")
                .style("fill-opacity", d => d.parent === root ? 1 : 0)
                .style("display", d => d.parent === root ? "inline" : "none")
                .text(d => d.data.name);

            zoomTo([root.x, root.y, root.r * 2]);

            function zoomTo(v) {
              const k = width / v[2];

              view = v;

              label.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
              node.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
              node.attr("r", d => d.r * k);
            }

            function zoom(d) {
              const focus0 = focus;

              focus = d;

              const transition = svg.transition()
                  .duration(d3.event.altKey ? 7500 : 750)
                  .tween("zoom", d => {
                    const i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2]);
                    return t => zoomTo(i(t));
                  });

              label
                .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
                .transition(transition)
                  .style("fill-opacity", d => d.parent === focus ? 1 : 0)
                  .on("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
                  .on("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
            }
        </script>
    </body>
</html>
"""  # noqa: E501


class BubblePack(NamedTuple):
    path: List[str]
    size: int
    value: int


def _aggregate_bubble_packs(data: List[BubblePack]) -> Dict[str, Any]:
    packable = {}

    # Aggregate files
    for bubble_file in data:
        pointer = packable
        for p in bubble_file.path[:-1]:
            pointer[p] = pointer.get(p, {})
            pointer = pointer[p]

        pointer[bubble_file.path[-1]] = {
            "name": bubble_file.path[-1],
            "value": bubble_file.value,
            "size": bubble_file.size,
            "/is_leaf": True,
        }

    return packable


def _rec_childrenizer(
    root_name: str, current_bubble_pack: Dict[str, Any]
) -> Dict[str, Any]:
    children = []
    for child_name, child_data in current_bubble_pack.items():
        if child_data.get("/is_leaf"):
            children.append(child_data)
            continue

        children.append(_rec_childrenizer(child_name, child_data))

    return {"name": root_name, "children": children}


class BubbleJSONDecoder(JSONEncoder):
    def default(self, o):
        if type(o) == int64:
            return int(o)
        return o


class BubblePackerDataSet(DefaultArgumentsMixIn, AbstractVersionedDataSet):
    DEFAULT_SAVE_ARGS = {"width": 932, "height": 600}

    def __init__(
        self, filepath: PurePath, version: Optional[Version] = None, *args, **kwargs
    ):
        super().__init__(filepath=filepath, version=version, *args, **kwargs)

    def _load(self) -> Any:
        raise WriteOnlyDataSet()

    def _save(self, data: List[BubblePack]) -> None:
        aggregated_bubble_packs = _aggregate_bubble_packs(data)
        childrenized_data = _rec_childrenizer("root", aggregated_bubble_packs)
        os.makedirs(os.path.dirname(self._filepath), exist_ok=True)
        max_domain = max([len(d.path) for d in data])
        max_heat = max([d.value for d in data])
        with open(self._filepath, "w+", encoding="utf8") as f:
            f.write(
                html_template
                % {
                    "json": json.dumps(childrenized_data, cls=BubbleJSONDecoder),
                    "max_domain": max_domain,
                    "max_heat": max_heat,
                    **self._save_args,
                }
            )

    def _describe(self) -> Dict[str, Any]:
        return dict(filepath=self._filepath)
