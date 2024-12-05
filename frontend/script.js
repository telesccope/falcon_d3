document.addEventListener("DOMContentLoaded", function() {
    const width = 800;
    const height = 600;

    const svg1 = d3.select("#graph1 svg")
        .attr("width", width)
        .attr("height", height);

    const svg2 = d3.select("#graph2 svg")
        .attr("width", width)
        .attr("height", height);

    const axiosInstance = axios.create({
        baseURL: 'https://travelassistant.uk' 
    });

    // 获取第一个图的数据
    axiosInstance.get('/api/graph')
        .then(response => {
            const data = response.data;
            console.log('data', data);

            drawGraph(svg1, data);

            // 获取第一个图的最短路径
            axiosInstance.get('/api/shortest-path/Node1/Node4')
                .then(response => {
                    const path = response.data;
                    console.log('path', path);
                    animatePath(svg1, path, data);
                });
        });

    // 获取第二个图的数据
    axiosInstance.get('/api/graph')
        .then(response => {
            const data = response.data;
            console.log('data', data);

            drawGraph(svg2, data);

            // 获取第二个图的最短路径
            axiosInstance.get('/api/shortest-path/Node2/Node5')
                .then(response => {
                    const path = response.data;
                    console.log('path', path);
                    animatePath(svg2, path, data);
                });
        });

    function drawGraph(svg, data) {
        const simulation = d3.forceSimulation(data.nodes)
            .force("link", d3.forceLink(data.links).id(d => d.id))
            .force("charge", d3.forceManyBody().strength(-400))
            .force("center", d3.forceCenter(width / 2, height / 2));

        const link = svg.append("g")
            .attr("stroke", "#999")
            .attr("stroke-opacity", 0.6)
            .selectAll("line")
            .data(data.links)
            .enter().append("line")
            .attr("stroke-width", 1.5);

        const node = svg.append("g")
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.5)
            .selectAll("circle")
            .data(data.nodes)
            .enter().append("circle")
            .attr("r", 8)
            .attr("fill", "#69b3a2")
            .call(drag(simulation));

        function drag(simulation) {
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

            return d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended);
        }

        simulation.on("tick", () => {
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node
                .attr("cx", d => d.x)
                .attr("cy", d => d.y);
        });
    }

    function animatePath(svg, path, data) {
        const pathLinks = [];
        for (let i = 0; i < path.length - 1; i++) {
            pathLinks.push(data.links.find(l => 
                (l.source.id === path[i] && l.target.id === path[i + 1]) ||
                (l.source.id === path[i + 1] && l.target.id === path[i])
            ));
        }

        pathLinks.forEach((linkData, index) => {
            setTimeout(() => {
                svg.selectAll("line")
                    .filter(d => d === linkData)
                    .transition()
                    .duration(1000)
                    .attrTween("stroke", function() {
                        return d3.interpolateRgb("#999", "red");
                    });
            }, index * 1500);
        });
    }
});
