// Main JavaScript functionality for Event Booking System

document.addEventListener("DOMContentLoaded", () => {
  // Initialize tooltips
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map((tooltipTriggerEl) => new window.bootstrap.Tooltip(tooltipTriggerEl))

  // Quantity selector functionality
  const quantityInputs = document.querySelectorAll(".quantity-input")
  quantityInputs.forEach((input) => {
    const minusBtn = input.parentElement.querySelector(".quantity-minus")
    const plusBtn = input.parentElement.querySelector(".quantity-plus")
    const priceElement = document.querySelector(".total-price")
    const unitPrice = Number.parseFloat(document.querySelector(".unit-price")?.textContent || 0)

    if (minusBtn) {
      minusBtn.addEventListener("click", () => {
        const currentValue = Number.parseInt(input.value)
        if (currentValue > 1) {
          input.value = currentValue - 1
          updateTotalPrice()
        }
      })
    }

    if (plusBtn) {
      plusBtn.addEventListener("click", () => {
        const currentValue = Number.parseInt(input.value)
        const maxTickets = Number.parseInt(input.getAttribute("max"))
        if (currentValue < maxTickets) {
          input.value = currentValue + 1
          updateTotalPrice()
        }
      })
    }

    input.addEventListener("change", updateTotalPrice)

    function updateTotalPrice() {
      if (priceElement && unitPrice) {
        const quantity = Number.parseInt(input.value)
        const total = unitPrice * quantity
        priceElement.textContent = `Rs. ${total.toFixed(2)}`
      }
    }
  })

  // Search functionality
  const searchForm = document.querySelector(".search-form")
  if (searchForm) {
    const searchInput = searchForm.querySelector('input[name="search"]')
    const categorySelect = searchForm.querySelector('select[name="category"]')

    // Auto-submit on category change
    if (categorySelect) {
      categorySelect.addEventListener("change", () => {
        searchForm.submit()
      })
    }
  }

  // Booking form validation
  const bookingForm = document.querySelector(".booking-form")
  if (bookingForm) {
    bookingForm.addEventListener("submit", (e) => {
      const quantity = Number.parseInt(document.querySelector('input[name="quantity"]').value)
      const availableTickets = Number.parseInt(document.querySelector(".available-tickets").textContent)

      if (quantity > availableTickets) {
        e.preventDefault()
        alert("Sorry, not enough tickets available!")
        return false
      }
    })
  }

  // Auto-hide alerts after 5 seconds
  const alerts = document.querySelectorAll(".alert:not(.alert-permanent)")
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.style.opacity = "0"
      setTimeout(() => {
        alert.remove()
      }, 300)
    }, 5000)
  })

  // Confirm delete actions
  const deleteButtons = document.querySelectorAll(".btn-delete, .delete-btn")
  deleteButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      if (!confirm("Are you sure you want to delete this item?")) {
        e.preventDefault()
        return false
      }
    })
  })

  // Image preview for file uploads
  const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]')
  imageInputs.forEach((input) => {
    input.addEventListener("change", (e) => {
      const file = e.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          let preview = document.querySelector(".image-preview")
          if (!preview) {
            preview = document.createElement("img")
            preview.className = "image-preview img-thumbnail mt-2"
            preview.style.maxWidth = "200px"
            input.parentElement.appendChild(preview)
          }
          preview.src = e.target.result
        }
        reader.readAsDataURL(file)
      }
    })
  })
})


