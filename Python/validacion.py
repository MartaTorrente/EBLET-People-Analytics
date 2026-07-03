def validar_dataset(df):

    print("\nVALIDACIÓN")

    print("Burnout:", df[[f"Q{i}" for i in range(21,30)]].mean().mean())
    print("Boreout:", df[[f"Q{i}" for i in range(30,39)]].mean().mean())
    print("Bienestar:", df[[f"Q{i}" for i in range(39,46)]].mean().mean())
    print("Rotación:", df[[f"Q{i}" for i in range(46,49)]].mean().mean())

    print("\nCORRELACIONES")
    print("Burnout vs bienestar:", df[[f"Q{i}" for i in range(21,30)]].mean(axis=1).corr(df[[f"Q{i}" for i in range(39,46)]].mean(axis=1)))