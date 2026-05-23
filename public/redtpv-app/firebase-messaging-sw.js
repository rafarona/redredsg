importScripts('https://www.gstatic.com/firebasejs/9.10.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.10.0/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: 'AIzaSyDQIQ4TK-AVtdzKb4WQ-6KSdFnHjCFcpuI',
  projectId: 'redpetvet25',
  messagingSenderId: '482372343054',
  appId: '1:482372343054:web:16489394762c2cc938f35f',
  authDomain: 'redpetvet25.firebaseapp.com',
  storageBucket: 'redpetvet25.appspot.com'
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