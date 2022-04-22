console.log('Let us check == and ===')
let a = 5
let b = "5"
let simple_compare = a == b
let strong_compare = a === b
console.log('5=="5" gives ' + simple_compare + ' because is makes type conversion')
console.log('But compare without type alignment: 5==="5" gives ' + strong_compare)

let string_vs_object = 'foo' == new String('foo')
let string_vs_object_strict = 'foo' === new String('foo')
console.log("'foo' == new string('foo') gives true: " + string_vs_object)
console.log("But 'foo' === new string('foo') gives false: " + string_vs_object_strict)

let c = { value: 5 }
let d = { value: 5 }
let e = c
console.log(`Basic compare of different objects with same properties gives false: ${c == d}`)
console.log(`Basic compare of objects REFERENCING to same item gives true: ${c == e}`)
console.log(`Scrict compare of objects REFERENCING TO same item gives also true: ${e === c}`)
