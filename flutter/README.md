# Wer Wie Was?
A Flutter based iOS application for retrieving page content.

---

## 📱 Features

- **Speech to Text:** Your speech is automatically transcribed using Whisper.
- **Automatic Page Parsing:** Parses various pages for later content retrieval.
- **Content Retrieval:** Uses RAG to retrieve information from parsed pages.

---

## 🛠 Prerequisites
Before you begin, ensure you have the following tools installed:

1. **Flutter SDK** (latest stable version)
   - Installation guide: [Flutter Installation](https://flutter.dev/docs/get-started/install)
2. **Xcode** (for iOS builds)
   - Download from the App Store or Apple Developer Tools.
3. **CocoaPods** (dependency manager for iOS)
   - Install via Terminal:
     ```bash
     sudo gem install cocoapods
     ```
4. **iOS Simulator** (optional) or a physical iOS device.

---

## 🚀 Installation Steps

Follow these steps to get the application up and running:

### 1. Clone the repository
```bash
git clone https://github.com/nischnei/werwiewas.git
cd flutter
```

### 2. Install Flutter dependencies
Ensure you are in the `flutter` directory and run:
```bash
flutter pub get
```

### 3. Install iOS dependencies
Navigate to the `ios` folder and run CocoaPods:
```bash
cd ios
pod install
cd ..
```

### 4. Run the application on iOS
Use the following command to launch the app on a connected device or simulator:
```bash
flutter run
```

- If you want to target a specific device, you can list available devices using:
  ```bash
  flutter devices
  ```

---

## 🧪 Testing
To run unit tests and widget tests, execute the following command:
```bash
flutter test
```

---

## 🐞 Troubleshooting
- **CocoaPods issues:**
  - Ensure you have Ruby installed and updated (`brew install ruby`)
  - Run `pod repo update` if dependencies fail.
- **Flutter not found:** Add Flutter to your system PATH.

---

## 📄 License
This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Contributors
- **[Nick Schneider](https://github.com/your-username)**


---

## 🤝 Support
For support, please open an issue.

---
