const bubbleContainer = document.querySelector('.bubble-container');

// Function to generate bubbles
function createBubble() {
    const bubble = document.createElement('div');
    bubble.classList.add('bubble');
    bubble.style.left = `${Math.random() * 100}vw`;
    bubble.style.width = `${Math.random() * 50 + 20}px`;
    bubble.style.height = bubble.style.width;
    bubble.style.animationDuration = `${Math.random() * 10 + 10}s`;

    bubbleContainer.appendChild(bubble);

    setTimeout(() => {
        bubble.remove();
    }, 20000);
}

// Generate multiple bubbles at intervals
setInterval(createBubble, 500);
