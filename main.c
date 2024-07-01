#include <stdio.h>
#include <IOKit/IOKitLib.h>

void printDeviceTree(io_registry_entry_t entry, int level) {
    io_iterator_t iterator;
    io_registry_entry_t child;
    kern_return_t result;

    CFStringRef name = IORegistryEntryCreateCFProperty(entry, CFSTR("name"), kCFAllocatorDefault, 0);
    if (name) {
        for (int i = 0; i < level; i++) {
            printf("  ");
        }
        printf("%s\n", CFStringGetCStringPtr(name, kCFStringEncodingUTF8));
        CFRelease(name);
    }

    result = IORegistryEntryCreateIterator(entry, kIOServicePlane, kIORegistryIterateRecursively, &iterator);
    if (result != KERN_SUCCESS) {
        return;
    }

    while ((child = IOIteratorNext(iterator))) {
        printDeviceTree(child, level + 1);
        IOObjectRelease(child);
    }

    IOObjectRelease(iterator);
}

int main() {
    io_registry_entry_t root = IORegistryGetRootEntry(kIOMasterPortDefault);
    if (!root) {
        fprintf(stderr, "Failed to get root entry\n");
        return 1;
    }

    printDeviceTree(root, 0);
    IOObjectRelease(root);

    return 0;
}
