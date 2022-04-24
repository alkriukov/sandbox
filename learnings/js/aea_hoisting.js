console.log('Hoisting is capability to use objects before they declared')
console.log('JS makes declarations in the beginning')

n = 6
console.log(n)
var n

hello('Alexey')
function hello(name) {
    console.log(`Hello ${name}`)
}

let me = new Person('Alexey')
me.introduce()
function Person(personName) {
    let name = personName
    this.introduce = function() {
        console.log(name)
    }
}
