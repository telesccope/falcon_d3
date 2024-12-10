let currentCoords = null;

// Fetch all graph filenames and populate the dropdown
fetch('/api/graph')
    .then(response => response.json())
    .then(graphIds => {
        const select = document.getElementById('graphSelect');
        graphIds.forEach(id => {
            const option = document.createElement('option');
            option.value = id;
            option.textContent = id;
            select.appendChild(option);
        });
    });

// Load the selected graph
document.getElementById('graphSelect').addEventListener('change', function() {
    const graphId = this.value;
    if (graphId) {
        fetch(`/api/graph/${graphId}`)
            .then(response => response.json())
            .then(graph => {
                drawGraph(graph);
            });
    }
});

function createPopup(nodeInfo) {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.className = 'popup-overlay';
    document.body.appendChild(overlay);

    // Create popup
    const popup = document.createElement('div');
    popup.className = 'popup';

    const popupContent = document.createElement('div');
    popupContent.className = 'popup-content';

    // Display node information
    const info = document.createElement('p');
    info.textContent = `Node Info: ${nodeInfo.id}`; // 使用 nodeInfo.id
    popupContent.appendChild(info);

    const message = document.createElement('p');
    message.textContent = 'Set this point as:';

    const startButton = document.createElement('button');
    startButton.textContent = 'Start';
    startButton.onclick = function() {
        document.getElementById("startCoord").value = nodeInfo.id;
        closePopup();
    };

    const endButton = document.createElement('button');
    endButton.textContent = 'End';
    endButton.onclick = function() {
        document.getElementById("endCoord").value = nodeInfo.id;
        closePopup();
    };

    popupContent.appendChild(message);
    popupContent.appendChild(startButton);
    popupContent.appendChild(endButton);
    popup.appendChild(popupContent);
    document.body.appendChild(popup);

    function closePopup() {
        document.body.removeChild(popup);
        document.body.removeChild(overlay);
    }

    overlay.onclick = closePopup;
}


function drawGraph(graph) {
    const svg = d3.select("#networkGraph svg")
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
            .attr("stroke", "#999")
            .attr("stroke-opacity", 0.6)
            .attr("stroke-width", 2);

        const node = g.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(nodes)
            .enter().append("circle")
            .attr("r", 20)
            .attr("fill", "black")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended))
                .on("click", function(event, d) {
                    event.stopPropagation();
                    currentCoords = { x: d.x, y: d.y };
                    console.log("Node clicked:", currentCoords); 
                    createPopup(d);
                });

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


document.getElementById('chooseAlgorithmButton').addEventListener('click', function() {
    const graphSelect = document.getElementById('graphSelect').value;
    const startCoord = document.getElementById('startCoord').value.trim();
    const endCoord = document.getElementById('endCoord').value.trim();

    if (!graphSelect) {
        alert('Please select a graph.');
        return;
    }

    if (!startCoord) {
        alert('Please select a start point.');
        return;
    }

    if (!endCoord) {
        alert('Please select an end point.');
        return;
    }

    const params = new URLSearchParams({
        graph: graphSelect,
        start: startCoord,
        end: endCoord
    });
    window.location.href = `select_algorithm.html?${params.toString()}`;
});
