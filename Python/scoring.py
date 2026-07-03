import pandas as pd

# =========================
# BURNOUT
# =========================
def burnout_exhaustion(df):
    return df[[f"Q{i}" for i in range(21, 24)]].mean(axis=1)

def burnout_cynicism(df):
    return df[[f"Q{i}" for i in range(24, 27)]].mean(axis=1)

def burnout_efficacy(df):
    return df[[f"Q{i}" for i in range(27, 30)]].mean(axis=1)

def burnout_global(df):
    return df[[f"Q{i}" for i in range(21, 30)]].mean(axis=1)


# =========================
# BOREOUT
# =========================
def boreout_disinterest(df):
    return df[[f"Q{i}" for i in range(30, 33)]].mean(axis=1)

def boreout_lack_challenge(df):
    return df[[f"Q{i}" for i in range(33, 36)]].mean(axis=1)

def boreout_underload(df):
    return df[[f"Q{i}" for i in range(36, 39)]].mean(axis=1)

def boreout_global(df):
    return df[[f"Q{i}" for i in range(30, 39)]].mean(axis=1)


# =========================
# WELLBEING
# =========================
def wellbeing_satisfaction(df):
    return df[[f"Q{i}" for i in range(39, 43)]].mean(axis=1)

def wellbeing_efficacy(df):
    return df[[f"Q{i}" for i in range(43, 46)]].mean(axis=1)

def wellbeing_global(df):
    return df[[f"Q{i}" for i in range(39, 46)]].mean(axis=1)


# =========================
# ROTATION
# =========================
def rotation_global(df):
    return df[[f"Q{i}" for i in range(46, 49)]].mean(axis=1)