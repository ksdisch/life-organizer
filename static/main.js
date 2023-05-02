function onCheckboxChange(event, completedList, originalList) {
    const checkbox = event.target;
    const listItem = checkbox.closest('.list-group-item');

    if (checkbox.checked) {
        completedList.appendChild(listItem);
    } else {
        originalList.appendChild(listItem);
    }
}

function onFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const checkbox = form.querySelector('input[type="checkbox"]');

    if (checkbox.checked) {
        form.status.value = "completed";
    } else {
        form.status.value = "incomplete";
    }

    form.submit();
}

// Tasks
const tasksList = document.querySelector('#tasks');
const completedTasksList = document.querySelector('#completed-tasks');
const taskForms = document.querySelectorAll('#tasks form, #completed-tasks form');
taskForms.forEach(form => {
    form.addEventListener('submit', onFormSubmit);
});

const taskCheckboxes = document.querySelectorAll('#tasks input[type="checkbox"], #completed-tasks input[type="checkbox"]');
taskCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', event => onCheckboxChange(event, completedTasksList, tasksList));
});

// Grocery items
const groceryItemsList = document.querySelector('#grocery_items');
const completedGroceryItemsList = document.querySelector('#completed-grocery-items');
const groceryForms = document.querySelectorAll('#grocery_items form, #completed-grocery-items form');
groceryForms.forEach(form => {
    form.addEventListener('submit', onFormSubmit);
});

const groceryCheckboxes = document.querySelectorAll('#grocery_items input[type="checkbox"], #completed-grocery-items input[type="checkbox"]');
groceryCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', event => onCheckboxChange(event, completedGroceryItemsList, groceryItemsList));
});

