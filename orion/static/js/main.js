document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        document.activeElement.blur();
    }

    if (event.key === 'F1') {
        const firstInput = document.querySelector('input, textarea');
        if (firstInput) {
            const commandName = firstInput.value.trim();
            if (commandName) {
                window.location.href = '/man/' + encodeURIComponent(commandName);
            }
        }
    }


    if (event.key === 'F2') {
        window.location.href = '/command';
    }

    if (event.target.tagName.toLowerCase() === 'input' || event.target.tagName.toLowerCase() === 'textarea') {
        return;
    }
    if (event.key === 'F4' || event.key === ',' || event.key === 'Backspace') {
        window.history.back();
    }
    if (event.key === '.') {
        const firstInput = document.querySelector('input, textarea');
        if (firstInput) {
            firstInput.focus();
        }
    }

    if (event.key === '`') {
        const homeLink = document.querySelector('a[href="/"]');
        if (homeLink) {
            homeLink.focus();
        }
    }

});