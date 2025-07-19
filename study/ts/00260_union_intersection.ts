console.log('Union types e.g. "number | null" are convenient when something can take or return values of few types')

function calcSqrt(x: number): number | null {
    let xSqrt = null;
    if (x >= 0) {
        xSqrt = Math.sqrt(x);
    }
    return xSqrt;
}

console.log(calcSqrt(16));
console.log(calcSqrt(0.01));
console.log(calcSqrt(-4));


type Printable = {
    print: () => void;
}

type Drawable = {
    draw: () => void;
}

console.log('\nType1 & Type2 is called type intersection')
type CmdGuiElement = Printable & Drawable;
let shapeElement: CmdGuiElement = {
    print: () => { console.log('Print element') },
    draw: () => { console.log('Draw element') }
}

shapeElement.print()
shapeElement.draw()
