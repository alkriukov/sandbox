console.log('Let\'s see ValueTypes and ReferenceTypes in JS');
console.log('ValueTypes are: Number, String, Boolean, Symbol, undefined and null');
let a = 5;
let b = 'Hello';
let c = true;
let d = null;
let e;

console.log(a + ' is a ' + typeof(a));
console.log(b + ' is a ' + typeof(b) + ' and has length ' + b.length);
console.log(c + ' is a ' + typeof(c));
console.log(d + ' is a ' + typeof(d));
console.log(e + ' is a ' + typeof(e));

console.log('ReferenceType examples are Objects...');
let me = {
    first_name: 'Alexey',
    last_name: 'Kryukov'
};
console.log(`Working with ${typeof(me)}, you can use .-notaion and bracket-notations: ${me.first_name} ${me['last_name']}`);

let g = Object('World');
console.log(`${g} is an ${typeof(g)}`);

console.log('...Functions...');
let sayHello = function() {
    console.log('Hello');
};
sayHello();
console.log(`${sayHello} is a ${typeof(sayHello)}`);

console.log('Other Reference data types are Collections, Arrays, Dates etc.');
console.log('But we\'ll cover them later');


