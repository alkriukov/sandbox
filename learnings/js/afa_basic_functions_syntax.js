function hello(message) {
    console.log('Hello')
    console.log('This is classic function declaration: function name(args) { body }')
    console.log(message)
}
hello('It can be invoked as name(args)')



const helloExpression = function(message) {
    console.log('Function expressions is e.g. const name = function(args) { body }')
    console.log(message)
}
helloExpression('It is invoked as name(args)')



const arrowFunction = message => {
    console.log('Instead of const   name = function(arg1, arg2)    { body }')
    console.log('we can use const   name =         (arg1, arg2) => { body }')
    console.log('If single arg:     name =          arg1        => { body }')
    console.log(message)
}
arrowFunction('And if body is single return line, then even shorter: name = arg => value')

let hypotenuse = (katet1, katet2) => Math.sqrt(katet1*katet1 + katet2*katet2)
console.log(hypotenuse(3, 4));



(function () {
    console.log('This is anonymous self-invoking function')
})();

(function (name) {
    console.log(`Hello ${name}`)
})('Alexey');


console.log('Factory function returns an object that can have e.g. fields and methods')
const createDot = function(coord_x, coord_y) {
    return {
        x: coord_x,
        y: coord_y,
        draw: function() {
            console.log(`Draw dot at x=${coord_x} y=${coord_x}`)
        }
    }
}
let dot1 = createDot(1, 1)
console.log(dot1.x)
dot1.draw()


console.log('Another way to create an object is Constructor function')
console.log('We can use public fields/member with this. and private with let')
const Dot = function(x, y) {
    let x1 = x
    let x2 = y
    this.draw = () => {
        console.log(`Draw dot at x=${x1} y=${x2}`)
    }
    this.moveTo = (x, y) => {
        x1 = x
        x2 = y
        this.draw()
    }
    Object.defineProperties(this, {
        'x': { get: () => x1 },
        'y': { get: () => x2 }
    })
}
console.log('Constructor function does not return an object. Object is created using new keyword')
let dot2 = new Dot(1, 1)
dot2.draw()
dot2.moveTo(2, 2)
console.log(dot2.x)

