const dogsContainer = document.getElementById("dogs");
const newDogBtn = document.getElementById("get-dog");
const clearBtn = document.getElementById("delete-dogs");
const errormessage = document.getElementById("error-message");
const loadingmessage = document.getElementById("loading-message");
const dogUri = "https://dog.ceo/api/breeds/image/random";

newDogBtn.addEventListener("click", async () => {
  let dog = await getDog();
  if (!dog) {
    errormessage.hidden = false;
    errormessage.style.color = "red";
    return;
  }
  errormessage.hidden = true;
  let newElement = document.createElement("img");
  newElement.classList = "dog-image";
  newElement.src = dog.message;
  dogsContainer.appendChild(newElement);

  clearBtn.hidden = showClear();
});

clearBtn.addEventListener("click", () => {
  while (dogsContainer.firstChild) {
    dogsContainer.removeChild(dogsContainer.firstChild);
  }
  clearBtn.hidden = !showClear();
});

async function getDog() {
  loadingmessage.hidden = false;
  let dogResponse = await axios(dogUri).then((response) =>
    response.status === 200 ? response.data : null
  );
  loadingmessage.hidden = true;
  return dogResponse;
}

function showClear() {
  return !dogsContainer.hasChildNodes;
}
