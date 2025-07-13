public class MainActivity extends AppCompatActivity {
    private Handler handler = new Handler();
    private long sessionStartTime;
    private static final long MAX_SESSION_MILLIS = 60 * 60 * 1000; // 1 hour

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        sessionStartTime = System.currentTimeMillis();
        handler.post(checkSessionRunnable);
    }

    private Runnable checkSessionRunnable = new Runnable() {
        @Override
        public void run() {
            long elapsed = System.currentTimeMillis() - sessionStartTime;
            if (elapsed >= MAX_SESSION_MILLIS) {
                // Show warning and close app
                Toast.makeText(MainActivity.this, "Time is up! The app will now close.", Toast.LENGTH_LONG).show();
                handler.postDelayed(() -> finishAffinity(), 2000); // Close after 2 seconds
            } else {
                handler.postDelayed(this, 1000); // Check every second
            }
        }
    };
}
