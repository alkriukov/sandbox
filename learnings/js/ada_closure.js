console.log('First of all, JS functions can access to surrounding environment')

const pi = 3.14159

function circlePermeter(radius) {
    console.log(2 * pi * radius)
}

function circleSquare(radius) {
    console.log(pi * radius * radius)
}
circlePermeter(5)
circleSquare(5)

let secretChecker = (key) => {
    let secretKey = key;
    return function checkKey(suggestedKey) { return key == suggestedKey }
}
{
let myKeyDefinedInSafePlace = '23lkjv0(U!@o4jqpw'
var checkMyAppKey = secretChecker(myKeyDefinedInSafePlace)
}

console.log('Key is undefined here: ' + checkMyAppKey.key)
console.log(checkMyAppKey('23lkjw0(U!@o4jqpw'))
console.log(checkMyAppKey('23lkjv0(U!@o4jqpw'))
