document.addEventListener('DOMContentLoaded', () => {
    // Copy code snippet buttons
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const textToCopy = btn.getAttribute('data-copy');
            if (textToCopy) {
                navigator.clipboard.writeText(textToCopy).then(() => {
                    const originalText = btn.textContent;
                    btn.textContent = 'Copied!';
                    btn.style.backgroundColor = 'var(--accent)';
                    btn.style.color = '#fff';
                    setTimeout(() => {
                        btn.textContent = originalText;
                        btn.style.backgroundColor = '';
                        btn.style.color = '';
                    }, 2000);
                }).catch(err => {
                    console.error('Copy failed', err);
                });
            }
        });
    });

    // Code sample dictionary
    const samples = {
        hello: {
            filename: 'hello.wc',
            code: `# hello.wc
display "Hello, World from Wordcode!"

set name to "Alice"
display "Welcome", name`,
            output: [
                'Hello, World from Wordcode!',
                'Welcome Alice'
            ]
        },
        fizzbuzz: {
            filename: 'fizzbuzz.wc',
            code: `# fizzbuzz.wc
set count to one

while count is less than or equal to fifteen
    if count modulo by fifteen is equal to zero then
        display "FizzBuzz"
    else if count modulo by three is equal to zero then
        display "Fizz"
    else if count modulo by five is equal to zero then
        display "Buzz"
    else
        display count
    end
    set count to count plus one
end`,
            output: [
                '1', '2', 'Fizz', '4', 'Buzz',
                'Fizz', '7', '8', 'Fizz', 'Buzz',
                '11', 'Fizz', '13', '14', 'FizzBuzz'
            ]
        },
        fibonacci: {
            filename: 'fibonacci.wc',
            code: `# fibonacci.wc
set a to zero
set b to one
set count to zero

repeat ten times
    display a
    set temp to a plus b
    set a to b
    set b to temp
end`,
            output: [
                '0', '1', '1', '2', '3', '5', '8', '13', '21', '34'
            ]
        }
    };

    let activeKey = 'hello';

    const tabButtons = document.querySelectorAll('.tab-btn');
    const exampleFilename = document.getElementById('example-filename');
    const exampleCodeDisplay = document.getElementById('example-code-display');
    const exampleOutputDisplay = document.getElementById('example-output-display');
    const runSampleBtn = document.getElementById('run-sample-btn');
    const copySampleBtn = document.getElementById('copy-sample-btn');

    function loadSample(key) {
        activeKey = key;
        const sample = samples[key];
        if (!sample) return;

        exampleFilename.textContent = sample.filename;
        exampleCodeDisplay.textContent = sample.code;

        // Reset output
        exampleOutputDisplay.innerHTML = '';
        sample.output.forEach(line => {
            const lineEl = document.createElement('div');
            lineEl.className = 'term-line output';
            lineEl.textContent = line;
            exampleOutputDisplay.appendChild(lineEl);
        });

        // Update active tab button
        tabButtons.forEach(btn => {
            if (btn.getAttribute('data-example') === key) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const key = btn.getAttribute('data-example');
            loadSample(key);
        });
    });

    if (runSampleBtn) {
        runSampleBtn.addEventListener('click', () => {
            const sample = samples[activeKey];
            if (!sample) return;

            exampleOutputDisplay.innerHTML = '<div class="term-line" style="color: #94a3b8;">> Running ' + sample.filename + '...</div>';

            setTimeout(() => {
                exampleOutputDisplay.innerHTML = '';
                sample.output.forEach(line => {
                    const lineEl = document.createElement('div');
                    lineEl.className = 'term-line output';
                    lineEl.textContent = line;
                    exampleOutputDisplay.appendChild(lineEl);
                });
            }, 300);
        });
    }

    if (copySampleBtn) {
        copySampleBtn.addEventListener('click', () => {
            const sample = samples[activeKey];
            if (sample) {
                navigator.clipboard.writeText(sample.code).then(() => {
                    const orig = copySampleBtn.textContent;
                    copySampleBtn.textContent = 'Copied!';
                    setTimeout(() => copySampleBtn.textContent = orig, 1500);
                });
            }
        });
    }
});
