// setTimeout(() => {
//   console.log("2 seconds passed");
// }, 2000);

// console.log("This logs stew");
// console.log("This logs Rice");
// function callBacks() {
//   console.log("Go to the market");
//   setTimeout(() => {
//   console.log("came back");
// }, 3000);
//   setTimeout(() => {
//   console.log("Cook stew");
// }, 6000);
//   setTimeout(() => {
//   console.log("Cook Rice");
// }, 4000);
// }
// callBacks()


const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// // wait(4000).then(() => console.log("1 second later"));
// wait(1000)
//   .then(() => { console.log("step 1"); return wait(1000); })
//   .then(() => { console.log("step 2"); return wait(1000); })
//   .then(() => console.log("step 3"))
//   .catch((error) => console.error("something failed:", error));

// async function get(){
//     console.log("step 1");
//     await wait(1000);
//     console.log("step 2");
// }
// get()

// async function Currency() {
//   try {
//     const response = await fetch("https://open.er-api.com/v6/latest/USD");
//     if (!response.ok) {
//       throw new Error(`API responded with status ${response.status}`);
//     }
//     const data = await response.json();
//     console.log(data);
//   } catch (error) {
//     console.error("Could not fetch data:", error.message);
//   }
// }

// Currency();
async function getRate(base,target) {
    try {
        const response=await fetch(`https://open.er-api.com/v6/latest/${base}`);
        if(!response.ok){
            throw new Error(`API response ${response.status}`)
        }
        const data=await response.json();
        console.log(data.rates[target])
    } catch (error) {
        console.error(`Could not fetch the currency ${base} to ${target}:`,error.message)
    }


}

async  function main() {
const rate = await getRate("USD","XAF")

if(rate !== null){
    console.log(`1 USD = ${rate} XAF`)
}
}


main ()