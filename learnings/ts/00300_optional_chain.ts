type Shape = {
    title: string
}

function shapeTitle(id: number): Shape | null {
    if (id < 0) {
        return null;
    }
    else {
        return { title: "Shape" }
    }
}

for (let i = -5; i < 5; i++) {
    let shape = shapeTitle(i)
    console.log(shape?.title);
}

const shapeNumbers = [1, 2, 3];
console.log(shapeNumbers?.[5]);
