def two_sum(nums: list[int], target: int) -> tuple[int, int]:
    for left in range(len(nums)):
        for right in range(left + 1, len(nums)):
            if nums[left] + nums[right] == target:
                return (right, left)
    return (-1, -1)

