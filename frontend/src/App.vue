<script>
import { ref,  } from 'vue'
import 'bootstrap/dist/css/bootstrap.css'

var card_id = ref("")
var current_deck_id = ref("")
var card_template_front = ref("")
var card_template_back = ref("")
var show_front = ref(false)
var show_back = ref(false)
var show_card_review = ref(false)
var show_deck_list = ref(true)
var show_card_list = ref(false)
var decks = ref([])
var cards = ref([])


async function getDecks() {
  try {
    var response = await fetch('http://localhost:8081/decks')
    var data = await response.json()
    decks.value = data
  } catch (error) {
    console.error('Error fetching deck list:', error)
  }
}

async function rateCard(vote, card_id) {
  try {
    var response = await fetch(`http://localhost:8081/card/${card_id}/rating`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        rating: vote
      })
    });
    if (response.ok == false) {
      console.error('Error sending vote:', response.status)
    } else {
      flipCard()
      getNextCard(current_deck_id.value)
    }
  }
  catch (error) {
    console.error('Error sending vote:', error);
  }
}

async function getCards(deck_id) {
  show_deck_list.value = !show_deck_list.value
  show_card_list.value = !show_card_list.value
  
  try {
    var resp = await fetch(`http://localhost:8081/deck/${deck_id}`, {method: 'GET'})
    var data = await resp.json()
    cards.value = data
    current_deck_id.value = deck_id
  } catch (error) {
    console.error('Error getting cards:', error)
  }
}

async function getNextCard(deck_id) {
  show_deck_list.value = false
  show_card_review.value = true
  show_front.value = true

  try {
    var resp = await fetch(`http://localhost:8081/deck/${deck_id}/next_card`)
    var data = await resp.json()
    card_id.value = data.id
    card_template_front.value = data.template.front
    card_template_back.value = data.template.back
    current_deck_id.value = deck_id
  } catch (error) {
    console.error('Error getting the card:', error)
  }
}

function flipCard() {
  show_back.value = !show_back.value
  show_front.value = !show_front.value
}

function backToMain() {
  show_deck_list.value = true
  show_card_list.value = false
  show_back.value = false
  show_front.value = false
  show_card_review.value = false
  card_id.value = ""
  current_deck_id.value = ""
  card_template_front.value = ""
  card_template_back.value = ""
  getDecks()
}


export default {
  setup() {
    getDecks()

    return {
      card_id,
      current_deck_id,
      card_template_front,
      card_template_back,
      decks,
      cards,
      rateCard,
      flipCard,
      getCards,
      getNextCard,
      backToMain,
      show_front,
      show_back,
      show_card_review,
      show_deck_list,
      show_card_list,
    }
  }
}
</script>


<template>
  <div>
  <!-- deck list -->
  <div id="deck-list" v-show="show_deck_list" class="decks">
    <ul>
      <li v-for="deck in decks" :key="deck">
        <button class="deck-info" @click="getCards(deck.id)">{{ deck.name }}</button>
        <button class="btn btn-primary" @click="getNextCard(deck.id)">{{ deck.name }}</button>
      </li>
    </ul>
  </div>

  <!-- card list  -->
  <div id="card-list" v-show="show_card_list" class="cards">
    <ul>
      <li v-for="(card, i) in cards" :key="i">{{card}}</li>
    </ul>
  </div>

  <!-- card review -->
  <div id="card-review" v-show="show_card_review" class="card text-center">
    <div class="card-body">
      <div v-html="card_template_front" v-show="show_front" class="card-text"></div>
      <div v-html="card_template_back" v-show="show_back" class="card-text"></div>
    </div>
    <button @click="flipCard">show</button>
    <div class="card-footer text-body-secondary" v-show="show_back">
      <button v-for="vote in 4" :key="vote" class="rate-button" @click="rateCard(vote, card_id)">Vote {{ vote }}</button>
    </div>
  </div>
  </div>

  <footer>
    <button @click="backToMain">back</button>
  </footer>
</template>

<style>
body{
  background-color: rgb(50, 52, 75);
  /* display: flex; */
  /* flex-direction: column;
  justify-content: center;
  align-items: center; */
  white-space: pre-line;
}
/* .card-front {
  margin-bottom: 20px;
} */
/* button {
  margin-right: 10px;
} */
.card {
  border: 2px solid darkgrey;
  border-radius: 10px;
  border-color: rgb(25, 18, 41);
  background-color: rgb(80, 82, 111);
  padding: 10px;
  width: 100%;
  /* height: fit-content; */
  /* max-width: 90%; */
}
.rate-button {
  background-color: slategrey;
  border-radius: 5px;
}
</style>
