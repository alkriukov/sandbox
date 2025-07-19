const putHello = () => {
    const helloText = "Hello";
    document.getElementById("say-hello-here").innerText = helloText;
}

window.onload = () => {
    putHello();
}
