class Solution:
    def trap(self, height: list[int]) -> int:
        if not height:
            return 0

        n = len(height)
        left = 0
        right = n - 1
        left_max = 0
        right_max = 0
        total_water = 0

        while left <= right:
            # Process the side with the smaller current height
            # because that side is the limiting factor for water calculation
            # at the current pointer's position.
            if height[left] < height[right]:
                # If current height[left] is greater than or equal to the max seen from left,
                # it means this bar can potentially hold water for bars to its right (if any are lower).
                # So, update left_max.
                if height[left] >= left_max:
                    left_max = height[left]
                else:
                    # If current height[left] is less than left_max, it means water can be trapped here.
                    # The water level is determined by left_max (since we know there's a taller bar on the right).
                    total_water += left_max - height[left]
                left += 1
            else:
                # Symmetrical logic for the right pointer
                if height[right] >= right_max:
                    right_max = height[right]
                else:
                    total_water += right_max - height[right]
                right -= 1
        
        return total_water
