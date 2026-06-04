import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class DatabaseService {
  static Database? _database;

  static Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  static Future<Database> _initDatabase() async {
    String path = join(await getDatabasesPath(), 'scenic_guide.db');
    return await openDatabase(
      path,
      version: 1,
      onCreate: (db, version) async {
        await db.execute('''
          CREATE TABLE chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            content TEXT,
            timestamp INTEGER
          )
        ''');
        await db.execute('''
          CREATE TABLE routes (
            id TEXT PRIMARY KEY,
            data TEXT,
            timestamp INTEGER
          )
        ''');
      },
    );
  }

  static Future<void> insertChatMessage(String role, String content) async {
    final db = await database;
    await db.insert('chat_history', {
      'role': role,
      'content': content,
      'timestamp': DateTime.now().millisecondsSinceEpoch,
    });
  }

  static Future<List<Map<String, dynamic>>> getChatHistory() async {
    final db = await database;
    return await db.query('chat_history', orderBy: 'timestamp ASC');
  }
}
