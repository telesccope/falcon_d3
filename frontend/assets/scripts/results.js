function drawGraph(svgElement, graph, steps, path) {
    const svg = d3.select(svgElement)
        .attr("viewBox", [0, 0, 800, 600])
        .attr("preserveAspectRatio", "xMidYMid meet");
    svg.selectAll("*").remove();

    const g = svg.append("g");

    const zoom = d3.zoom()
        .scaleExtent([0.1, 5])
        .on("zoom", (event) => g.attr("transform", event.transform));

    svg.call(zoom);

    const simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(d => d.id).distance(150))
        .force("charge", d3.forceManyBody().strength(-300))
        .force("center", d3.forceCenter(400, 300))
        .force("collide", d3.forceCollide().radius(30));

    if (graph.features) {
        const nodes = [];
        const links = [];
        const pathSet = new Set(path.map(coord => coord.toString()));
        const stepSet = new Set(steps.flatMap(step => step.map(coord => coord.toString())));

        graph.features.forEach(feature => {
            feature.geometry.coordinates.forEach((coord, i) => {
                const roundedCoord = coord.map(c => Math.round(c * 1000) / 1000);
                const nodeId = roundedCoord.toString();
                if (!nodes.some(n => n.id === nodeId)) {
                    nodes.push({ id: nodeId, x: roundedCoord[0], y: roundedCoord[1] });
                }
                if (i > 0) {
                    links.push({ source: feature.geometry.coordinates[i - 1].map(c => Math.round(c * 1000) / 1000).toString(), target: nodeId });
                }
            });
        });

        const link = g.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(links)
            .enter().append("line")
            .attr("stroke", "#aaa")
            .attr("stroke-opacity", 0.6)
            .attr("stroke-width", 2);

        const node = g.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(nodes)
            .enter().append("circle")
            .attr("r", 20)
            .attr("fill", d => pathSet.has(d.id) ? "#ff7f0e" : (stepSet.has(d.id) ? "#2ca02c" : "#1f77b4"))
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));

        simulation
            .nodes(nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(links);

        function ticked() {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);
        }

        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }

        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
    } else {
        console.error("No features found in the graph data.");
    }
}



async function visualize(graphId, algorithm, start, end, svgSelector, infoSelector) {
    const graph = await fetchGraph(graphId);
    const result = await fetchShortestPath(graphId, algorithm, start, end);
    drawGraph(svgSelector, graph, result.steps, result.path);

    const infoDiv = document.querySelector(infoSelector);
    infoDiv.innerHTML = `
        <div class="bar"><div class="bar-inner" style="width:${result.time_taken * 100}px"></div><span class="bar-label">Time: ${result.time_taken}</span></div>
        <div class="bar"><div class="bar-inner" style="width:${result.steps.length * 10}px"></div><span class="bar-label">Steps: ${result.steps.length}</span></div>
        <div class="bar"><div class="bar-inner" style="width:${result.path.length * 10}px"></div><span class="bar-label">Path: ${result.path.length}</span></div>
        <div class="bar"><div class="bar-inner" style="width:${result.total_weight}px"></div><span class="bar-label">Weight: ${result.total_weight}</span></div>
    `;
}
function getUrlParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        graph: params.get('graph'),
        start: params.get('start'),
        end: params.get('end'),
        algorithm1: params.get('algorithm1'),
        algorithm2: params.get('algorithm2')
    };
}

async function fetchGraph(graphId) {
    try {
        const response = await fetch(`/api/graph/${graphId}`);
        if (!response.ok) {
            throw new Error('Graph not found');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching graph:', error);
    }
}

async function fetchShortestPath(graph, algorithm, start, end) {
    try {
        const response = await fetch(`/api/shortest-path/${graph}/${algorithm}/${start}/${end}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching shortest path:', error);
    }
}

const params = getUrlParams();
if (params.algorithm1) {
    visualize(params.graph, params.algorithm1, params.start, params.end, "#networkGraph1 svg", "#networkGraph1 .info");
}
if (params.algorithm2) {
    visualize(params.graph, params.algorithm2, params.start, params.end, "#networkGraph2 svg", "#networkGraph2 .info");
}
