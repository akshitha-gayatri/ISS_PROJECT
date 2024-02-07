// document.addEventListener('DOMContentLoaded', function () {
//     const loginForm = document.getElementById('login-form');
//     const loginMessage = document.getElementById('login-message');
//     const dropArea = document.getElementById('drop-area');
//     const fileInput = document.getElementById('fileInput');
//     const selectedImagesContainer = document.getElementById('selected-images-container');
//     const selectedImagesPreview = document.getElementById('selected-images-preview');
//     const confirmSelectionButton = document.getElementById('confirm-selection-button');
//     const randomVideoContainer = document.getElementById('random-video-container');

//     // Function to handle file selection
//     function handleFiles(files) {
//         for (const file of files) {
//             if (file.type.match('image')) {
//                 const reader = new FileReader();
//                 reader.onload = function (event) {
//                     const img = document.createElement('img');
//                     img.src = event.target.result;
//                     img.style.maxWidth = '100px'; // Adjust image size as needed
//                     selectedImagesPreview.appendChild(img);
//                 };
//                 reader.readAsDataURL(file);
//             }
//         }
//     }

//     // Handle file input change event
//     fileInput.addEventListener('change', function (e) {
//         const files = e.target.files;
//         handleFiles(files);
//         selectedImagesContainer.style.display = 'block';
//     });

//     // Handle drag and drop events
//     dropArea.addEventListener('dragover', function (e) {
//         e.preventDefault();
//         dropArea.classList.add('active');
//     });

//     dropArea.addEventListener('dragleave', function (e) {
//         e.preventDefault();
//         dropArea.classList.remove('active');
//     });

//     dropArea.addEventListener('drop', function (e) {
//         e.preventDefault();
//         dropArea.classList.remove('active');
//         const files = e.dataTransfer.files;
//         handleFiles(files);
//         selectedImagesContainer.style.display = 'block';
//     });

//     // Confirm selection and proceed to create video page
//     confirmSelectionButton.addEventListener('click', function () {
//         // Add logic to proceed to create video page with selected images
//         // For now, just log a message
//         console.log('Proceed to create video with selected images');
//         randomVideoContainer.style.display = 'block'; // Show the random video container
//         playVideo(); // Play the video
//     });

//     // Login form handling
//     loginForm.addEventListener('submit', function (e) {
//         e.preventDefault();
//         const username = document.getElementById('username').value;
//         const password = document.getElementById('password').value;

//         if (username === 'user' && password === '1234') {
//             loginMessage.textContent = 'Login Success';
//             setTimeout(function () {
//                 window.open('createvideo.html', '_blank'); // Redirect to create video page
//             }, 1000); // Delay for 1 second (optional)
//         } else if (username === 'admin' && password === 'admin') {
//             loginMessage.textContent = 'Admin Login Success';
//             setTimeout(function () {
//                 window.open('createvideo.html', '_blank'); // Redirect to create video page
//             }, 1000); // Delay for 1 second (optional)
//         } else {
//             loginMessage.textContent = 'Invalid Username or Password';
//         }
//     });

//     // Function to play the video
//     // function playVideo() {
//     //     // Replace 'video.mp4' with your video file name
//     //     const videoPath = 'video.mp4';
//     //     window.open(videoPath, '_blank');
//     //     return false;
//     // }
// });





document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('login-form');
    const loginMessage = document.getElementById('login-message');
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('fileInput');
    const selectedImagesContainer = document.getElementById('selected-images-container');
    const selectedImagesPreview = document.getElementById('selected-images-preview');
    const confirmSelectionButton = document.getElementById('confirm-selection-button');
    const randomVideoContainer = document.getElementById('random-video-container');

    // Function to handle file selection
    function handleFiles(files) {
        for (const file of files) {
            if (file.type.match('image')) {
                const reader = new FileReader();
                reader.onload = function (event) {
                    const img = document.createElement('img');
                    img.src = event.target.result;
                    img.style.maxWidth = '100px'; // Adjust image size as needed
                    selectedImagesPreview.appendChild(img);
                };
                reader.readAsDataURL(file);
            }
        }
    }

    // Handle file input change event
    fileInput.addEventListener('change', function (e) {
        const files = e.target.files;
        handleFiles(files);
        selectedImagesContainer.style.display = 'block';
    });

    // Handle drag and drop events
    dropArea.addEventListener('dragover', function (e) {
        e.preventDefault();
        dropArea.classList.add('active');
    });

    dropArea.addEventListener('dragleave', function (e) {
        e.preventDefault();
        dropArea.classList.remove('active');
    });

    dropArea.addEventListener('drop', function (e) {
        e.preventDefault();
        dropArea.classList.remove('active');
        const files = e.dataTransfer.files;
        handleFiles(files);
        selectedImagesContainer.style.display = 'block';
    });

    // Confirm selection and proceed to create video page
    confirmSelectionButton.addEventListener('click', function () {
        // Add logic to proceed to create video page with selected images
        // For now, just log a message
        console.log('Proceed to create video with selected images');
        randomVideoContainer.style.display = 'block'; // Show the random video container
        playVideo(); // Play the video
    });

    // Login form handling
    loginForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (username === 'user' && password === '1234') {
            loginMessage.textContent = 'Login Success';
            setTimeout(function () {
                window.open('createvideo.html', '_blank'); // Redirect to create video page
            }, 1000); // Delay for 1 second (optional)
        } else if (username === 'admin' && password === 'admin') {
            loginMessage.textContent = 'Admin Login Success';
            setTimeout(function () {
                window.open('createvideo.html', '_blank'); // Redirect to create video page
            }, 1000); // Delay for 1 second (optional)
        } else {
            loginMessage.textContent = 'Invalid Username or Password';
        }
    });

    // Function to play the video
    // function playVideo() {
    //     // Replace 'video.mp4' with your video file name
    //     const videoPath = 'video.mp4';
    //     window.open(videoPath, '_blank');
    //     return false;
    // }
});