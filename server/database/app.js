const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const  cors = require('cors')
const app = express()
const port = 3030;

app.use(cors())
app.use(require('body-parser').urlencoded({ extended: false }));

const reviews_data = JSON.parse(fs.readFileSync("data/reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("data/dealerships.json", 'utf8'));

// For local development, skip MongoDB connection and use JSON data directly
// mongoose.connect("mongodb://mongo_db:27017/",{'dbName':'dealershipsDB'});


// Use JSON data directly for local development
let reviews = reviews_data['reviews'];
let dealerships = dealerships_data['dealerships'];

console.log(`Loaded ${dealerships.length} dealerships and ${reviews.length} reviews from JSON files`);


// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API")
});

// Express route to fetch all reviews
app.get('/fetchReviews', (req, res) => {
  try {
    res.json(reviews);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', (req, res) => {
  try {
    const dealerId = parseInt(req.params.id);
    const dealerReviews = reviews.filter(review => review.dealership === dealerId);
    res.json(dealerReviews);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer reviews' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', (req, res) => {
  try {
    res.json(dealerships);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', (req, res) => {
  try {
    const stateDealerships = dealerships.filter(dealer => dealer.state === req.params.state);
    res.json(stateDealerships);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', (req, res) => {
  try {
    const dealerId = parseInt(req.params.id);
    const dealer = dealerships.find(dealer => dealer.id === dealerId);
    res.json(dealer);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer by id' });
  }
});

//Express route to insert review
app.post('/insert_review', express.json(), (req, res) => {
  try {
    data = req.body;
    
    // Find the highest existing ID and increment
    let new_id = 1;
    if (reviews.length > 0) {
      new_id = Math.max(...reviews.map(r => r.id)) + 1;
    }

    const newReview = {
      "id": new_id,
      "name": data['name'],
      "dealership": parseInt(data['dealership']),
      "review": data['review'],
      "purchase": data['purchase'],
      "purchase_date": data['purchase_date'],
      "car_make": data['car_make'],
      "car_model": data['car_model'],
      "car_year": parseInt(data['car_year']),
    };

    // Add to in-memory array
    reviews.push(newReview);
    res.json(newReview);
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
