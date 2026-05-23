importScripts('https://www.gstatic.com/firebasejs/9.10.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.10.0/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: 'AIzaSyDApqP8ZmBS1Hu7hQ5u2mZxBnVjX8iSCDY',
  projectId: 'redpetvet25',
  messagingSenderId: '482372343054',
  appId: '1:482372343054:web:a4ce3016ca2f796538f35f',
  authDomain: 'redpetvet25.firebaseapp.com',
  storageBucket: 'redpetvet25.firebasestorage.app'
});

const messaging = firebase.messaging();

// Optional: Handle background messages
messaging.onBackgroundMessage((payload) => {
  console.log('Received background message:', payload);

  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: '/icons/Icon-192.png'
  };

  return self.registration.showNotification(notificationTitle, notificationOptions);
}); 