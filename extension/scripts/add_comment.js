let comment_element = document.createElement("div");
comment_element.classList.add("newtral_comment");
comment_element.innerHTML = "Finding other news sources...";
document.body.append(comment_element);

let url = "http://localhost:5000/get_comment?" + new URLSearchParams({"article": location.href}).toString();
console.log("Request URL:", url);

fetch(url)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.text();
  })
  .then(result => {
    comment_element.innerText = result;
  })
  .catch(error => {
    console.error('Fetch error:', error);
  });
