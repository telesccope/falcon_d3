const algorithmInput = document.getElementById('algorithmInput');
const algorithmList = document.getElementById('algorithmList');
const selectedAlgorithms = document.getElementById('selectedAlgorithms');

let selectedAlgorithm1 = null;
let selectedAlgorithm2 = null;

function getUrlParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        graph: params.get('graph'),
        start: params.get('start'),
        end: params.get('end')
    };
}

const params = getUrlParams();
const graph = params.graph;
const start = params.start;
const end = params.end;

async function fetchAlgorithms() {
    try {
        const response = await fetch('/api/algorithms');
        const algorithms = await response.json();
        algorithms.forEach(algorithm => {
            const option = document.createElement('option');
            option.value = algorithm;
            algorithmList.appendChild(option);
        });
    } catch (error) {
        console.error('Error fetching algorithms:', error);
    }
}

algorithmInput.addEventListener('change', function() {
    const value = algorithmInput.value;
    if (!selectedAlgorithm1) {
        selectedAlgorithm1 = value;
        document.getElementById('algorithm1').querySelector('span').textContent = value;
    } else if (!selectedAlgorithm2) {
        selectedAlgorithm2 = value;
        document.getElementById('algorithm2').querySelector('span').textContent = value;
    }
    algorithmInput.value = '';
});

function removeAlgorithm(number) {
    if (number === 1) {
        selectedAlgorithm1 = null;
        document.getElementById('algorithm1').querySelector('span').textContent = 'Algorithm 1';
    } else if (number === 2) {
        selectedAlgorithm2 = null;
        document.getElementById('algorithm2').querySelector('span').textContent = 'Algorithm 2';
    }
}

document.getElementById('comparisonButton').addEventListener('click', function() {
    if (!selectedAlgorithm1 || !selectedAlgorithm2) {
        alert('Please select two algorithms.');
        return;
    }
    const params = new URLSearchParams({
        graph: graph,
        start: start,
        end: end,
        algorithm1: selectedAlgorithm1,
        algorithm2: selectedAlgorithm2
    });
    window.location.href = `results.html?${params.toString()}`;
});

fetchAlgorithms();