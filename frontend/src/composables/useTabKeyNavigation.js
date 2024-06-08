import { onMounted,onBeforeUnmount } from 'vue'
export default function useTabKeyNavigation(tabsListRef) {
    const moveToFirstTab = () => {
        const tab = tabsListRef.value.children[0];
        selectTab(tab);
    };

    const moveToLastTab = () => {
        const lastTab = tabsListRef.value.children[tabsListRef.value.children.length - 1];
        selectTab(lastTab);
    };

    const moveTabLeft = () => {
        const currentTabIndex = getCurrentTabIndex();
        let previousTab = tabsListRef.value.children[currentTabIndex - 1];

        if (!previousTab) {
            moveToLastTab();
        } else {
            selectTab(previousTab);
        }
    };

    const moveTabRight = () => {
        const currentTabIndex = getCurrentTabIndex();
        let nextTab = tabsListRef.value.children[currentTabIndex + 1];

        if (!nextTab) {
            moveToFirstTab();
        } else {
            selectTab(nextTab);
        }
    };

    const getCurrentTabIndex = () => {
        const activeElement = document.activeElement;
        return Array.from(tabsListRef.value.children).findIndex((tab) =>
            tab.contains(activeElement)
        );
    };

    const selectTab = (tab) => {
        const link = tab.querySelector("a");
        link.focus();
        if (!tab.dataset.noClickOnKeyNavigation) {
            link.click();
        }
    };

    const handleKeyDown = (event) => {
        switch (event.key) {
            case 'ArrowLeft':
                moveTabLeft();
                break;
            case 'ArrowRight':
                moveTabRight();
                break;
            case 'Home':
                moveToFirstTab();
                break;
            case 'End':
                moveToLastTab();
                break;
        }
    };

    onMounted(() => {
        tabsListRef.value.addEventListener('keydown', handleKeyDown);
    });

    onBeforeUnmount(() => {
        tabsListRef.value.removeEventListener('keydown', handleKeyDown);
    });

    return {
        getCurrentTabIndex,
    };
}