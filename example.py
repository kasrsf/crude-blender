from src import crude_blender

if __name__ == '__main__':
    distil_profiles = crude_blender.load_from_csv()
    blend_profile = crude_blender.blend_oils(distil_profiles, 'Mixed Sweet Blend', 2, 'CNRL Light Sweet Synthetic', 4)
    print(blend_profile.to_string())