import numpy as np


class FindMinimum:
    def __init__(self, arr, n):
        self.arr = arr
        self.n = n
        self.localMin(self.arr, self.n)

    def localMinUtil(self, arr, low, high, n):

        # Find index of middle element
        mid = low + (high - low) // 2

        # Compare middle element with its
        # neighbours (if neighbours exist)
        if (mid == 0 or arr[mid - 1] > arr[mid] and
                mid == n - 1 or arr[mid] < arr[mid + 1]):
            return mid

            # If middle element is not minima and its left
        # neighbour is smaller than it, then left half
        # must have a local minima.
        elif mid > 0 and arr[mid - 1] < arr[mid]:
            return self.localMinUtil(arr, low, mid - 1, n)

            # If middle element is not minima and its right
        # neighbour is smaller than it, then right half
        # must have a local minima.
        return self.localMinUtil(arr, mid + 1, high, n)

        # A wrapper over recursive function localMinUtil()

    def localMin(self, arr, n):

        return self.localMinUtil(arr, 0, n - 1, n)

    def local_maxima_mask(self, vec):
        """
        Get a mask of all points in vec which are local maxima
        :param vec: A real-valued vector
        :return: A boolean mask of the same size where True elements correspond to maxima.
        """
        mask = np.zeros(vec.shape, dtype=np.bool)
        greater_than_the_last = np.diff(vec) > 0  # N-1
        mask[1:] = greater_than_the_last
        mask[:-1] &= ~greater_than_the_last
        return mask


