

$("#ingredientSearch").on("change", function(){
    // Make a request to search for ingredients
    if ($("#ingredientSearch").val() != ""){
        axios.get('/ingredients/search/' + $("#ingredientSearch").val())
        .then(function (response) {
            // handle success
            $("#ingredient-container").empty();
            const ingredients = response.data.hints
            for(const ingredient of ingredients){
                $("#ingredient-container").append(`
                    <div class='col-lg-3 col-md-4 col-6 my-auto'>
                    <div class='ingredient-card'>
                    <img src='${ingredient.food.image || "/static/images/default-ingredient-img.png"}' alt='food image'/>
                    <h6>${ingredient.food.label}</h6>
                    <i data-food-id ='${ingredient.food.foodId}' class="fa-solid fa-plus add-ingredient"></i>
                    </div>
                    </div
                    `
                )
            }
            console.log(response);
        })
        .catch(function (error) {
            // handle error
            console.log(error);
            $("#ingredient-container").empty();
            $("#ingredient-container").html(
                "<p>Something went wrong please try again</p>"
            )
        })
    }

});

$("#ingredient-container").on("click", "i", function(e){
    const foodId = $(this)[0].dataset.foodId;
    const parentElem = $(this).parent();
    
    if ($(this).hasClass("add-ingredient") == true){
        axios.get(`/users/ingredients/add/${foodId}`)
        .then(function (response) {
            console.log(response.data);
            if (response.data == "Success"){
                parentElem.html("<p>Ingredient Saved!</p>")
                
            }
            else if(response.data == "exists"){
                parentElem.html("<p>This ingredient is already in your fridge</p>")
            }
        })
        .catch(function (error) {
            $('.results').text("Something Went wrong please try again later");
        })
    }

    else if($(this).hasClass("remove-ingredient") == true){
        axios.get(`/users/ingredients/remove/${foodId}`)
        .then(function (response) {
            console.log(response.data);
            if (response.data == "Success"){
                $('.results').text("Ingredient removed");
                console.log(parentElem);
                parentElem.html("<p>Ingredient Removed!</p>")
            }
        })
        .catch(function (error) {
            $('.results').text("Something Went wrong please try again later");
        })
    }

    else if($(this).hasClass("add-to-pot") == true){
        $("#recipe-container").append(parentElem.parent());
        parentElem.children(".add-to-pot").hide();
        parentElem.children("p").hide();
    }
});

$("#recipe-container").on("click", "i", function(e){
    const parentElem = $(this).parent();
    $("#ingredient-container").append(parentElem.parent());
    parentElem.children(".add-to-pot").show();
    parentElem.children("p").show();
});

$(".find-recipe").on("click", function(e){
    e.preventDefault();
    let $allIngredientCards = $("#recipe-container").find("h6");
    console.log($allIngredientCards);
    let potIngredients = [];
    
    for(let ingredient of $allIngredientCards){
        potIngredients.push(ingredient.innerText);
        console.log(potIngredients);
    }

    potIngredients.reduce((f, s) => `${f},${s}`)

    // $.ajax({
    //     url: "/recipes/search",
    //     type: "GET",
    //     data: {
    //         ingredients: potIngredients,
    //         recipeType: $("#recipeType").val()
    //     },
    //     success: function (response) {
    //         console.log(response)
    //     }
    // });

    axios.get('/recipes/search', {
        params: {
            ingredients: potIngredients,
            recipeType: $("#recipeType").val()
        }
      }).then(function(response){
        console.log(response)
      })
    // axios({
    // method: 'post',
    // url: '/recipes/search',
    // data: {
    //     ingredients: potIngredients,
    //     recipeType: $("#recipeType").val()
    // }
    // });
});
