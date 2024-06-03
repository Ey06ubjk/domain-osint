document.addEventListener("DOMContentLoaded", function() {
    var startTime;  // Declare the startTime variable
    var timerInterval;  // Declare the timerInterval variable
    var abortController = null; // Declare an abort controller

    // Adding CSS dynamically for layout
    var style = document.createElement('style');
    style.type = 'text/css';
    style.innerHTML = `
        #finished-text-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        #finished-text {
            margin-right: 20px; /* Adjust spacing as needed */
        }
        .download-all-btn-container {
            margin-top: 10px; /* For vertical layout */
        }
    `;
    document.head.appendChild(style);

    var navLinks = document.querySelectorAll('.nav-link'); // Select all nav links
    var currentLocation = window.location.pathname; // Get the current path

    navLinks.forEach(function(link) {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active'); // Add 'active' class to the matching link
        }
    });

    document.getElementById('selectAll').addEventListener('click', function() {
        var checkboxes = document.querySelectorAll('.checkbox-grid input[type="checkbox"]');
        var allChecked = Array.from(checkboxes).every(checkbox => checkbox.checked);
        checkboxes.forEach(function(checkbox) {
            checkbox.checked = !allChecked;
        });
    });

    var runButton = document.getElementById("run-button");
    if (runButton) {
        runButton.addEventListener("click", function() {
            shouldAbortProcessing = false;
            deleteFiles()
            abortController = new AbortController(); // Instantiate the abort controller for this run

            var oldFinishedTextContainer = document.getElementById("finished-text-container");
            if (oldFinishedTextContainer) {      // Remove old finished text container if exists
                oldFinishedTextContainer.parentNode.removeChild(oldFinishedTextContainer);
            }
        
            var domainName = document.getElementById("domain-input").value.trim();
            var domainNameOrg = document.getElementById("domain-input-org").value.trim();
            var domainPage = document.getElementById("domain-page").value.trim();
            
            // Basic pattern match for domain names (simple validation)
            var domainPattern = /^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            var domainPatternOrg = /^[a-zA-Z0-9.-]/;
            var domainPatternPage = /^[1-9]\d*$/;
            if (!domainPattern.test(domainName)) {
                alert("Please enter a valid domain name, e.g., example.com");
                return false; // Exit the function if the domain name doesn't match the pattern
            }

            var checkboxUsername = document.getElementById("checkbox-username"); 

            if (checkboxUsername.checked) {
                if (!domainPatternOrg.test(domainNameOrg)) {
                    alert("Please enter a valid company name, e.g., Example");
                    return false; // Exit the function if the domain name doesn't match the pattern
                }
                // Check if domainPage is not empty, then it must be a valid number
                if (domainPage !== "" && !domainPatternPage.test(domainPage)) {
                    alert("Please enter a valid page number, e.g., 2");
                    return false; // Exit the function if the page number is invalid
                }
            }
            domainPage = parseInt(domainPage, 10);

            startTime = new Date();  // Set the startTime when the run begins
            document.getElementById("loading-indicator").style.display = 'block';

            // Start a timer that updates every second
            timerInterval = setInterval(function() {
                var currentTime = new Date();
                var timeDiff = currentTime - startTime; 
                var minutes = Math.floor(timeDiff / 60000);  // 1 minute = 60000 milliseconds
                var seconds = Math.floor((timeDiff % 60000) / 1000);  // Remaining seconds
                var minutesFormatted = (minutes < 10) ? "0" + minutes : minutes;
                var secondsFormatted = (seconds < 10) ? "0" + seconds : seconds;

                // Optionally hide the run button
                document.getElementById("run-button").style.display = 'none';
              
                // Update the text content with the formatted time string
                document.getElementById("output-container").innerHTML = "";
                document.getElementById("loading-indicator").textContent = 
                    'Running... ' + minutesFormatted + ':' + secondsFormatted + '. Do not click anything!'; 
            }, 99); // Update interval every 99 milliseconds to show the milliseconds counting

            // Define the order of the checks
            var orderedChecks = ['host', 'ws_office', 'whois', 'subscraper', 'wafw00f', 'shcheck', 'wpscan', 'username', 'email', 'ssl', 'tls', 'port', 'hping'];
            var checkboxes = {
                checkbox1: document.getElementById("checkbox-host").checked,
                checkbox2: document.getElementById("checkbox-ws_office").checked,
                checkbox3: document.getElementById("checkbox-whois").checked,
                checkbox4: document.getElementById("checkbox-subscraper").checked,
                checkbox5: document.getElementById("checkbox-wafw00f").checked,
                checkbox6: document.getElementById("checkbox-shcheck").checked,
                checkbox7: document.getElementById("checkbox-wpscan").checked,
                checkbox8: document.getElementById("checkbox-username").checked,
                checkbox9: document.getElementById("checkbox-email").checked,
                checkbox10: document.getElementById("checkbox-ssl").checked,
                checkbox11: document.getElementById("checkbox-tls").checked,
                checkbox12: document.getElementById("checkbox-port").checked,
                checkbox13: document.getElementById("checkbox-hping").checked,
            };

            fetch('/run_checks', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ domain: domainName, domainorg: domainNameOrg, checkboxes: checkboxes, page: domainPage }),
                signal: abortController.signal // Pass the signal to the fetch request
            })
            .then(response => {
                if (shouldAbortProcessing) return; // Early exit if processing should be aborted
                return response.json();
            })
            .then(data => {
                if (shouldAbortProcessing) return;
                clearInterval(timerInterval);
            
                var endTime = new Date();
                var timeDiff = endTime - startTime;
                var minutes = Math.floor(timeDiff / 60000);
                var seconds = Math.floor((timeDiff % 60000) / 1000);
                var minutesFormatted = (minutes < 10) ? "0" + minutes : minutes;
                var secondsFormatted = (seconds < 10) ? "0" + seconds : seconds;
            
                document.getElementById("loading-indicator").textContent = '';
            
                var finishedTextContainer = document.createElement("div");
                finishedTextContainer.id = "finished-text-container";
                finishedTextContainer.style.display = 'flex';
                finishedTextContainer.style.alignItems = 'flex-start';
            
                var finishedText = document.createElement("span");
                finishedText.id = "finished-text";
                finishedText.textContent = 'Scan completed, preparing to display results...';
            
                finishedTextContainer.appendChild(finishedText);
                document.getElementById("output-container").style.display = 'none';
            
                // Prepend the finished text container before the output container
                var outputContainer = document.getElementById("output-container");
                outputContainer.parentNode.insertBefore(finishedTextContainer, outputContainer);
            
                setTimeout(() => {
                    finishedText.textContent = 'Finished in ' + minutesFormatted + ':' + secondsFormatted + ', Results are ready!';
                    document.getElementById("output-container").style.display = 'block';
                    
                    // Create a download link for all results
                    var downloadAllLink = document.createElement("a");
                    downloadAllLink.href = '/download_results';
                    downloadAllLink.textContent = "Download All Results";
                    downloadAllLink.className = "btn btn-primary";
                    finishedTextContainer.appendChild(downloadAllLink);
            
                    // Iterate over each check and display results
                    orderedChecks.forEach(function(check) {
                        if (data.outputs.hasOwnProperty(check)) {
                            var outputDiv = document.createElement("div");
                            outputDiv.className = "output-section";
            
                            var resultPre = document.createElement("pre");
                            resultPre.textContent = data.outputs[check];
                            
                            // Create a download link for each check
                            var downloadLink = document.createElement("a");
                            downloadLink.href = data.file_paths[check];
                            downloadLink.textContent = "Download " + check.toUpperCase() + " Results";
                            downloadLink.className = "btn";
                          
                            // Create a collapsible button for each check
                            var collapsibleButton = document.createElement("button");
                            collapsibleButton.className = "collapsible";
                            collapsibleButton.innerText = "Results: " + check.toUpperCase();
            
                            outputDiv.appendChild(collapsibleButton);
                            var contentDiv = document.createElement("div");
                            contentDiv.className = "content";
                            contentDiv.appendChild(resultPre);
                            contentDiv.appendChild(downloadLink);
                            outputDiv.appendChild(contentDiv);
                            document.getElementById("output-container").appendChild(outputDiv);
                            
                            // Add event listener to toggle visibility of results
                            collapsibleButton.addEventListener("click", function() {
                                this.classList.toggle("active");
                                var content = this.nextElementSibling;
                                if (content.style.display === "block") {
                                    content.style.display = "none";
                                } else {
                                    content.style.display = "block";
                                }
                            });
                        }
                    });
                    document.getElementById("run-button").style.display = 'block'; // Show the run button again
                }, 4000); 
            })

            .catch(error => {
                console.error('Error:', error);
                if (error.name === "AbortError") {
                    console.log("Fetch aborted.");
                    document.getElementById("loading-indicator").textContent = 'Operation cancelled.';
                } else {
                    document.getElementById("loading-indicator").textContent = 'An error occurred.';
                }
                document.getElementById("loading-indicator").style.display = 'none';
                clearInterval(timerInterval);
            })
            .finally(() => {
                if (shouldAbortProcessing) return; // Ensure UI is not reset if already handled
            });
        });
    }

    function deleteFiles() {
        fetch('/delete_files', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Files deleted successfully.");
            } else {
                console.error("Failed to delete files: ", data.error);
            }
        })
        .catch(error => {
            console.error("Error deleting files: ", error);
        });
    }

    window.confirmReset = function() {
        var confirmation = confirm("Are you sure you want to reset and start over?\nIf any, current results will be deleted.");
        if (confirmation) {
            if (abortController) {
                abortController.abort();
                shouldAbortProcessing = true; // Set the flag to stop further processing
            }
            // Reset UI and internal state
            clearInterval(timerInterval);
            deleteFiles()
            document.getElementById("loading-indicator").style.display = 'none';
            document.getElementById("domain-page").value = "";  // Clear the domain input field
            document.getElementById("domain-input").value = "";  // Clear the domain input field
            document.getElementById("domain-input-org").value = "";  // Clear the domain input field
            document.getElementById("output-container").innerHTML = '';

            document.getElementById("run-button").style.display = 'block'; // Show the run button again
            var oldFinishedTextContainer = document.getElementById("finished-text-container");
            if (oldFinishedTextContainer) {      // Remove old finished text container if exists
                oldFinishedTextContainer.parentNode.removeChild(oldFinishedTextContainer);
            }
            const checkboxes = document.querySelectorAll('input[type="checkbox"]');  // Uncheck all checkboxes
            checkboxes.forEach(checkbox => {
                checkbox.checked = false;
            });
        }
    };
});