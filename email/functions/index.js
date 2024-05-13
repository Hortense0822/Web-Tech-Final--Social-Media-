const functions = require("firebase-functions");
const admin = require("firebase-admin");
const nodemailer = require("nodemailer");

admin.initializeApp();

exports.sendEmailNotification = functions.firestore
    .document("posts/{postId}")
    .onCreate(async (snap, context) => {
      const post = snap.data();
      const usersRef = admin.firestore().collection("students");
      const users = await usersRef.get();
      const emails = users.docs.map((user) => user.data().email);

      const transporter = nodemailer.createTransport({
        host: "smtp.gmail.com",
        port: 465,
        secure: true,
        auth: {
          user: "umubyeyihortense@gmail.com",
          pass: "epjcdnlfrpjdfqjg",
        },
      });

      const mailOptions = {
        from: "Ashesi Social Network <" + "umubyeyihortense@gmail.com" + ">",
        to: emails.join(","),
        subject: "New post created!",
        text: `A new post has been created by: ${post.ownerEmail}.`,
      };

      await transporter.sendMail(mailOptions);
    });