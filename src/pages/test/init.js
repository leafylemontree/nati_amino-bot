console.log("\nApp is ready\n");

document.querySelector(".in-control div button").addEventListener("click", ()=>{
    let text = document.querySelector(".in-control div input").value;
    client.write(`node: ${text}`);
  });
