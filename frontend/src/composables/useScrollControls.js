import { ref, onMounted, onBeforeUnmount } from "vue";

export default function useScrollControls(
  tabsListRef,
  { leftButtonRef = null, rightButtonRef = null } = {}
) {
  let isDragging = false;
  const showLeftButton = ref(false);
  const showRightButton = ref(false);

  const handleScroll = () => {
    updateScrollButtons();
  };

  const updateScrollButtons = () => {
    const container = tabsListRef.value;
    if (!container) return;

    const maxScrollValue = container.scrollWidth - container.clientWidth;

    showLeftButton.value = container.scrollLeft > 0;

    showRightButton.value = container.scrollLeft < maxScrollValue;

    if (leftButtonRef) {
      leftButtonRef.value.classList.toggle("hidden", container.scrollLeft <= 0);
    }

    if (rightButtonRef) {
      rightButtonRef.value.classList.toggle(
        "hidden",
        container.scrollLeft >= maxScrollValue
      );
    }
  };

  const startDrag = () => {
    isDragging = true;
    tabsListRef.value.classList.add("!scroll-auto");
    tabsListRef.value.classList.add("!cursor-grabbing");
  };

  const endDrag = () => {
    isDragging = false;
    tabsListRef.value.classList.remove("!scroll-auto");
    tabsListRef.value.classList.remove("!cursor-grabbing");
  };

  const handleLeftButtonClick = () => {
    const container = tabsListRef.value;
    container.scrollLeft -= 200;
    updateScrollButtons();
  };

  const handleRightButtonClick = () => {
    const container = tabsListRef.value;
    container.scrollLeft += 200;
    updateScrollButtons();
  };

  let dragEventListenersAdded = false;

  const addEventListeners = () => {
    tabsListRef.value.addEventListener("scroll", handleScroll);

    // Agregar event listeners solo si no es un dispositivo móvil
    const isMobile = window.matchMedia("(max-width: 768px)").matches;
    if (!isMobile) {
      tabsListRef.value.addEventListener("mousedown", startDrag);
      tabsListRef.value.addEventListener("mouseup", endDrag);
      tabsListRef.value.addEventListener("mouseleave", endDrag);
      tabsListRef.value.addEventListener("mousemove", handleDrag);
      dragEventListenersAdded = true;
    }

    if (leftButtonRef) {
      leftButtonRef.value.addEventListener("click", handleLeftButtonClick);
    }
    if (rightButtonRef) {
      rightButtonRef.value.addEventListener("click", handleRightButtonClick);
    }


  };

  const removeEventListeners = () => {
    tabsListRef.value.removeEventListener("scroll", handleScroll);

    if (dragEventListenersAdded) {
      tabsListRef.value.removeEventListener("mousedown", startDrag);
      tabsListRef.value.removeEventListener("mouseup", endDrag);
      tabsListRef.value.removeEventListener("mouseleave", endDrag);
      tabsListRef.value.removeEventListener("mousemove", handleDrag);
    }

    if (leftButtonRef) {
      leftButtonRef.value.removeEventListener("click", handleLeftButtonClick);
    }
    if (rightButtonRef) {
      rightButtonRef.value.removeEventListener("click", handleRightButtonClick);
    }
  };

  const handleDrag = (event) => {
    if (!isDragging) return;
    event.preventDefault();
    tabsListRef.value.scrollLeft -= event.movementX;
    updateScrollButtons();
  };

  onMounted(() => {
    addEventListeners();
    updateScrollButtons();
  });

  onBeforeUnmount(() => {
    removeEventListeners();
  });

  return {
    showLeftButton,
    showRightButton,
    handleScrollLeft: () => {
      const container = tabsListRef.value;
      container.scrollLeft -= 200;
      updateScrollButtons();
    },
    handleScrollRight: () => {
      const container = tabsListRef.value;
      container.scrollLeft += 200;
      updateScrollButtons();
    },
  };
}
