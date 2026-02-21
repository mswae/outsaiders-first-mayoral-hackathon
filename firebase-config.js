import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-firestore.js";

const firebaseConfig = {
    apiKey: "AIzaSyAlP99hk1atPqua1hP_G_XZMoA1TbWqvsU",
    authDomain: "peopulse-4a1d4.firebaseapp.com",
    projectId: "peopulse-4a1d4",
    storageBucket: "peopulse-4a1d4.firebasestorage.app",
    messagingSenderId: "590735399776",
    appId: "1:590735399776:web:9735c339297dd1ba3c1c05"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export { db, firebaseConfig };