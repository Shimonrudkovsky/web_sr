<script>
import { ref } from 'vue'

const card_id = ref("")
const card_fields = ref([])
const card_template_front = ref("")
const card_template_back = ref("")
var show_front = ref(true)
var show_back = ref(false)


async function getValues() {
  try {
    const response = await fetch('http://localhost:8080/card')
    const data = await response.json()
    card_id.value = data.id
    card_fields.value = data.fields
    card_template_front.value = data.template.front
    card_template_back.value = data.template.back
  } catch (error) {
    console.error('Error fetching values:', error)
  }
}

async function rateCard(vote, card_id) {
  try {
    const response = await fetch(`http://localhost:8080/card/${card_id}/rate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        rate: vote
      })
    });
    const data = await response.json()
    this.votes = data.votes
  }
  catch (error) {
    console.error('Error sending vote:', error);
  }
}


export default {
  setup() {
    getValues()

    return {
      card_id,
      card_fields,
      card_template_front,
      card_template_back,
      show_front,
      show_back,
      rateCard
    }
  }
}
</script>


<template>
  <div>
  <div id="app" class="card">
    <div v-html="card_template_front" v-show="show_front" class="card-front"></div>
    <div v-html="card_template_back" v-show="show_back" class="card-back"></div>
    <button @click="show_back = !show_back; show_front = !show_front">show</button>
    <div v-show="show_back">
      <button v-for="vote in 4" :key="vote" class="rate-button" @click="rateCard(vote, card_id)">Vote {{ vote }}</button>
    </div>
  </div>
  </div>
</template>

<style>
body{
  background-color: rgb(50, 52, 75);
  /* display: flex; */
  flex-direction: column;
  justify-content: center;
  align-items: center;
  white-space: pre-line;
}
.card-front {
  margin-bottom: 20px;
}
button {
  margin-right: 10px;
}
.card {
  /* position: absolute; */
  border: 2px solid darkgrey;
  border-radius: 10px;
  border-color: rgb(25, 18, 41);
  background-color: rgb(80, 82, 111);
  padding: 10px;
  width: 100%;
  height: fit-content;
  max-width: 90%;
}
.rate-button {
  background-color: slategrey;
  border-radius: 5px;
}
</style>
