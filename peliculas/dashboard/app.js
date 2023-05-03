$(document).ready(function () {
  // INFOCARDS

  var cardData = [
    {
      id: 1,
      text: "Ventas al contado",
      count: 25,
      money: 270987.63,
    },
    {
      id: 2,
      text: "Ventas a Credito",
      count: 0,
      money: 0.0,
    },
    {
      id: 3,
      text: "Cobros",
      count: 0,
      money: 0.0,
    },
  ];

  var acomulated = {
    id: 4,
    text: "Acomulado",
    count: "2023/04/02",
    money: 270987.63,
  };

  const getData = async () => {
    try {
      const res = await fetch(`https://pokeapi.co/api/v2/pokemon`);
      const data = await res.json();

      cardData.forEach((element) => {
        $(".info-cards").append(`
                  <div class="card">
                   <div class="card-body">
                    <h5 class="card-title" id="">${element.count}</h5>
                    <p class="card-text">${element.text}</p>
                    <a href="#" class="btn btn-dark redirect-info" style="width: 100%;">${element.money}</a>
                    </div>
                  </div>`);
      });

      $(".info-cards").append(`
                  <div class="card">
                   <div class="card-body">
                    <h5 class="card-title" id="">${acomulated.count}</h5>
                    <p class="card-text">${acomulated.text}</p>
                    <a href="#" class="btn btn-dark redirect-info" style="width: 100%;">${acomulated.money}</a>
                    </div>
                  </div>`);

      data.results.forEach((element) => {
        $(".t-data").append(`
            <tr>
            <td><span>${element.weight}</span></td>
            <td><span>${element.name}</span></td>
            <td><span>${element.order}</span></td>
            <td><span>${element.order}</span></td>
            </tr>
            `);
      });

      $(".t-data").append(`
            <tr class="total">
            <td><span>${data.results.weight}</span></td>
            <td><span>${data.results.name}</span></td>
            <td><span>${data.results.order}</span></td>
            <td><span>${data.results.order}</span></td>
            </tr>
            `);
    } catch (error) {
      console.log(error);
    }
  };

  getData();

  setInterval(async () => {
    $(".info-cards").empty();
    $(".t-data").empty();
    $(".t-data").append(`
    <tr>
     <th><span>FECHA</span></th>
     <th><span>CONTADO</span></th>
     <th><span>CREDITO</span></th>
     <th><span>COBROS</span></th>
    </tr>
    `);
    getData();
  }, 60000);
});
