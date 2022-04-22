console.log('In addition to var, now we have also let and const')
console.log('In most cases we\'ll use let. Block visibility, ok to change')

let clientServiceLevel = 'Regular'
clientServiceLevel = 'Key'
console.log(clientServiceLevel)

const pi = 3.14
console.log(`${pi} is an ${typeof(pi)}`)
console.log('Constants aren\'t are not for changing. pi = 3.14159 will cause an error')

console.log('Note that const Reference types allow to modify item they are pointing to')
const my_const = {
    pi: 3.14
}
my_const.pi = 3.14159
my_const.e = 2.7271
console.log(my_const)
console.log('const prohibits reassignment to another object. E.g. my_const = { pi: 3.14159, e: 2.7271 } will cause an error')

{
    var name = 'Alexey'
    let shortName = 'Alex'
    console.log(`let declared variables can be used within the block: ${shortName}`)
}
console.log(`var declared variables are visible outside the block: ${name}`)
