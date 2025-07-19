console.log('Spread operator is ...array')
const simpleArr = [1, 2, 3];
const anotherArr = [...simpleArr, 4, ...[5, 6]];
anotherArr.pop();
for (let i in anotherArr) {
    console.log(anotherArr[i]);
};

const jobs = [
    {processed_items: 52, jobType: 'read', isActive: false},
    {processed_items: 35, jobType: 'write', isActive: true},
    {processed_items: 13, jobType: 'listen', isActive: true},
];
console.log('Very typical operation is to do something for each element in array');
console.log('Form new array from some items, form new array from all items adjusted somehow, etc.');

console.log('JS arrays have filter, map, and reduce functions which simlify the code');
const active_jobs1 = jobs.filter( function(job) { return job.isActive });
const active_jobs2     = jobs.filter(          job =>        job.isActive  );
console.log(active_jobs1)
console.log(active_jobs2)

// Map allows to form new array, where initial element mapped to something else
const items = active_jobs1.map(job => job.processed_items);
console.log(items);

const processed_total = jobs.reduce((total, value, index, jobs) => total+=value.processed_items, 0);
console.log(processed_total);
