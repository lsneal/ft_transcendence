var generateBtn = document.getElementById('generateSP');
generateBtn.addEventListener('click', myFetcher);

function myFetcher() {
fetch('https://localhost')
  .then(
    function(response) {
      if (response.status !== 200) {
        console.log('Looks like there was a problem. Status Code: ' +
          response.status);
        return;
      }
      response.json().then(function(data) {
        console.log(data);
        document.getElementById('w3review').value = data;
      });
    }
  )
  .catch(function(err) {
    console.log('Fetch Error :-S', err);
  })
}
myFetcher();