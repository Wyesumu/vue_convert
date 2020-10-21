<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Cart</h1>
        <hr>
        <div class='row border-bottom'>
            <div class='col font-weight-bold'>Name</div>
            <div class='col font-weight-bold'>Quantity</div>
            <div class='col font-weight-bold'>Currency</div>
            <div class='col font-weight-bold'>Price</div>
            <div class='col'></div>
        </div>
        <div class='row border-bottom' v-for="(good, index) in goods" :key="index">
            <div class='col'>{{ good.name }}</div>
            <div class='col'>{{ good.quantity }}</div>
            <div class='col'>{{ good.currency }}</div>
            <div class='col'>{{ good.price }}</div>
            <div class='col'><button type="button" @click="onDeleteGood(good)" class="btn btn-danger btn">Delete</button></div>
        </div>
        <form @submit="onSubmit">
            <div class='row my-2'>
                <div class='col'><input placeholder="Name" class='form-control' v-model='addGoodForm.name'></div>
                <div class='col'><input type='number' min=1 placeholder="Quantity" class='form-control' v-model='addGoodForm.quantity'></div>
                <div class='col'>
                    <select class="custom-select" v-model='addGoodForm.currency'>
                      <option value="RUB">RUB</option>
                      <option value="USD">USD</option>
                      <option value="EUR">EUR</option>
                    </select>
                </div>
                <div class='col'><input type='number' step=0.1 min=1 placeholder="Price" class='form-control' v-model='addGoodForm.price'></div>

                <button type="submit" class="btn btn-success btn ml-auto">Add good</button>
            </div>
        </form>
        <div class='row'>
            <div class='col'>
                <p>{{ result_calculate }}</p>
            </div>
            <div class='col'>
                <button type="submit" @click="onCaculate()" class="btn btn-info btn ml-auto">Calculate</button>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      goods: [],
      addGoodForm: {
        id: '',
        name: '',
        quantity: '',
        currency: '',
        price: '',
      },
      result_calculate: '',
    };
  },
  methods: {
    getGoods() {
      const path = 'http://127.0.0.1:5000/user/cart';
      axios.get(path)
        .then((res) => {
          this.goods = res.data.goods;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addGood(payload) {
      const path = 'http://127.0.0.1:5000/user/cart';
      axios.post(path, payload)
        .then(() => {
          this.getGoods();
        })
        .catch((error) => {
          console.log(error);
          this.getGoods();
        });
    },
    initForm() {
      this.addGoodForm.name = '';
      this.addGoodForm.quantity = '';
      this.addGoodForm.currency = '';
      this.addGoodForm.price = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      const payload = {
        name: this.addGoodForm.name,
        quantity: this.addGoodForm.quantity,
        currency: this.addGoodForm.currency,
        price: this.addGoodForm.price,
      };
      this.addGood(payload);
      this.initForm();
    },
    removeGood(goodID) {
      const path = `http://127.0.0.1:5000/user/cart/delete_good/${goodID}`;
      axios.delete(path)
        .then(() => {
          this.getGoods();
        })
        .catch((error) => {
          console.error(error);
          this.getGoods();
        });
    },
    onDeleteGood(good) {
      this.removeGood(good.id);
    },
    calculateCurrency(payload) {
      const path = 'http://127.0.0.1:5000/user/cart/calculate';
      axios.post(path, payload)
        .then((result) => {
            console.log(result);
            this.result_calculate = result['data']['message'];
          //this.getGoods();
        })
        .catch((error) => {
          console.log(error);
          //this.getGoods();
        });
    },
    onCaculate() {
        const payload = {
            goods: this.goods,
        }
        this.calculateCurrency(payload);
    },
  },
  created() {
    this.getGoods();
  },
};
</script>
