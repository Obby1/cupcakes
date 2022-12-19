// alert("working js") 



const BASE_URL = "http://127.0.0.1:5000/api";

function generateCupcakeHTML(cupcake) {
    return `
      <div data-cupcake-id=${cupcake.id}>
        <li>
          ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
          <button class="delete-button">X</button>
        </li>
        <img class="Cupcake-img"
              src="${cupcake.image}"
              alt="(no image provided)">
      </div>
    `;
  }
  

async function showInitialCupcakes() {
    const response = await axios.get(`${BASE_URL}/cupcakes`);
//   try response.json.cupcakes
    for (let cupcakeData of response.data.cupcakes) {

      let newCupcake = $(generateCupcakeHTML(cupcakeData));

      $("#cupcakes-list").append(newCupcake);

    }
  }

//select Jquery delete button, append API to delete cupcake, 
//append dom to remove deleted cupcake

$('#new-cupcake-form').on("submit", async function(evt){
    evt.preventDefault();

    // collect values from html form
    // make sure JQuery values are properly selected ($ + ( '#  info ') ), error code 500 showed up previously
    let flavor = $('#form-flavor').val();
    let size = $('#form-size').val();
    let rating = $('#form-rating').val();
    let image = $('#form-image').val();

    // ping API with new cupcake info
    // {flavor:flavor, size:size, rating:rating, image:image} also works
    const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, 
    {flavor, size, rating, image});
   
    // generate HTML for new cupcake and append DOM
    let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
    $("#cupcakes-list").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
});

$('#cupcakes-list').on("click", ".delete-button", async function (evt){
    evt.preventDefault();
    let $cupcake = $(evt.target).closest("div");
    let $cupcakeId = $cupcake.attr("data-cupcake-id");

    await axios.delete(`${BASE_URL}/cupcakes/${$cupcakeId}`);
    $cupcake.remove();
});

// new_cupcake = Cupcake(flavor = request.json["flavor"], size = request.json["size"], 
//     rating = request.json["rating"], image = request.json["image"])


  

showInitialCupcakes()


// $('.delete-todo').click(deleteTodo)

// async function deleteTodo() {
//   const id = $(this).data('id')
//   await axios.delete(`/api/todos/${id}`)
//   $(this).parent().remove()
// }