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
            .attr("fill", d => 
                pathSet.has(d.id) 
                    ? "#FFA500"  
                    : (stepSet.has(d.id) 
                        ? "#6FCF97"  
                        : "#CCCCCC"  
                    )
            )

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

    if (!graph || !result) {
        console.error("Failed to fetch graph or shortest path data.");
        return;
    }

    drawGraph(svgSelector, graph, result.steps, result.path);

    const infoDiv = document.querySelector(infoSelector);
    infoDiv.innerHTML = `
        <div class="bar">
            <div class="bar-inner time" style="width: 0;"></div>
            <span class="bar-label">Time(ms): ${result.time_taken}</span>
        </div>
        <div class="bar">
            <div class="bar-inner steps" style="width: 0;"></div>
            <span class="bar-label">Steps: ${result.steps.length}</span>
        </div>
        <div class="bar">
            <div class="bar-inner path" style="width: 0;"></div>
            <span class="bar-label">Path: ${result.path.length}</span>
        </div>
        <div class="bar">
            <div class="bar-inner weight" style="width: 0;"></div>
            <span class="bar-label">Weight: ${result.total_weight}</span>
        </div>
    `;

    // 使用 setTimeout 确保动画触发
    setTimeout(() => {
        const timeBar = document.querySelector(`${infoSelector} .bar-inner.time`);
        const stepsBar = document.querySelector(`${infoSelector} .bar-inner.steps`);
        const pathBar = document.querySelector(`${infoSelector} .bar-inner.path`);
        const weightBar = document.querySelector(`${infoSelector} .bar-inner.weight`);

        if (timeBar) timeBar.style.width = `${result.time_taken * 100}px`;
        if (stepsBar) stepsBar.style.width = `${result.steps.length * 10}px`;
        if (pathBar) pathBar.style.width = `${result.path.length * 10}px`;
        if (weightBar) weightBar.style.width = `${result.total_weight}px`;
    }, 100); // 延迟 100ms 以确保动画生效
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

function setAlgorithmTitles(params) {
    const algorithmTitle1 = document.getElementById("algorithmTitle1");
    const algorithmTitle2 = document.getElementById("algorithmTitle2");

    if (params.algorithm1) {
        algorithmTitle1.textContent = `Algorithm 1: ${params.algorithm1}`;
    } else {
        algorithmTitle1.textContent = "Algorithm 1: Not specified";
    }

    if (params.algorithm2) {
        algorithmTitle2.textContent = `Algorithm 2: ${params.algorithm2}`;
    } else {
        algorithmTitle2.textContent = "Algorithm 2: Not specified";
    }
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
setAlgorithmTitles(params);
if (params.algorithm1) {
    visualize(params.graph, params.algorithm1, params.start, params.end, "#networkGraph1 svg", "#networkGraph1 .info");
}
if (params.algorithm2) {
    visualize(params.graph, params.algorithm2, params.start, params.end, "#networkGraph2 svg", "#networkGraph2 .info");
}
