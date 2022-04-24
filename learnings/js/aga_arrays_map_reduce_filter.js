let simpleArr = [1, 2, 3]
let anotherArr = [...simpleArr, 4, ...[5, 6]]
anotherArr.pop()
for (i in anotherArr) {
    console.log(anotherArr[i])
}

let jobs = [
    {processed_items: 52, jobType: 'read', isActive: false},
    {processed_items: 35, jobType: 'write', isActive: true},
    {processed_items: 13, jobType: 'listen', isActive: true},
]
console.log('Very typical operations is for each element in array do something')
console.log('Form new array from some items, for new array with adjusted items etc.')

console.log('JS arrays have filter, map and reduce functions that simlifies the code')
let active_jobs = jobs.filter( function(job) { return job.isActive })
active_jobs     = jobs.filter(          job =>        job.isActive  )

// Map allows to form new array, where initial element mapped to something else
items = active_jobs.map(job => job.processed_items)
console.log(items)

processed_total = jobs.reduce((total, value, index, jobs) => total+=value.processed_items, 0)
console.log(processed_total)
