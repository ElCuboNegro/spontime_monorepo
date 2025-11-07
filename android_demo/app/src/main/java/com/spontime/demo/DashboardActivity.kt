package com.spontime.demo

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import com.google.android.material.button.MaterialButton
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.google.android.material.textfield.TextInputEditText
import com.spontime.demo.api.CreatePlanRequest
import com.spontime.demo.api.Plan
import com.spontime.demo.api.RetrofitClient
import kotlinx.coroutines.launch

class DashboardActivity : AppCompatActivity() {

    private lateinit var recyclerView: RecyclerView
    private lateinit var swipeRefresh: SwipeRefreshLayout
    private lateinit var adapter: PlansAdapter
    private lateinit var profileButton: MaterialButton
    private lateinit var createPlanButton: MaterialButton
    private lateinit var logoutButton: MaterialButton

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_dashboard)

        initViews()
        setupRecyclerView()
        setupListeners()
        loadPlans()
    }

    private fun initViews() {
        recyclerView = findViewById(R.id.plans_recycler_view)
        swipeRefresh = findViewById(R.id.swipe_refresh)
        profileButton = findViewById(R.id.profile_button)
        createPlanButton = findViewById(R.id.create_plan_button)
        logoutButton = findViewById(R.id.logout_button)
    }

    private fun setupRecyclerView() {
        adapter = PlansAdapter()
        recyclerView.layoutManager = LinearLayoutManager(this)
        recyclerView.adapter = adapter
    }

    private fun setupListeners() {
        swipeRefresh.setOnRefreshListener {
            loadPlans()
        }

        profileButton.setOnClickListener {
            showProfile()
        }

        createPlanButton.setOnClickListener {
            showCreatePlanDialog()
        }

        logoutButton.setOnClickListener {
            performLogout()
        }
    }

    private fun loadPlans() {
        swipeRefresh.isRefreshing = true

        lifecycleScope.launch {
            try {
                val response = RetrofitClient.apiService.getPlans()
                swipeRefresh.isRefreshing = false

                if (response.isSuccessful && response.body() != null) {
                    val plans = response.body()!!.results
                    adapter.submitList(plans)
                } else {
                    Toast.makeText(
                        this@DashboardActivity,
                        "Failed to load plans",
                        Toast.LENGTH_SHORT
                    ).show()
                }
            } catch (e: Exception) {
                swipeRefresh.isRefreshing = false
                Toast.makeText(
                    this@DashboardActivity,
                    "Error: ${e.message}",
                    Toast.LENGTH_LONG
                ).show()
            }
        }
    }

    private fun showProfile() {
        lifecycleScope.launch {
            try {
                val response = RetrofitClient.apiService.getProfile()
                if (response.isSuccessful && response.body() != null) {
                    val user = response.body()!!
                    MaterialAlertDialogBuilder(this@DashboardActivity)
                        .setTitle("Profile")
                        .setMessage(
                            "Handle: ${user.handle}\n" +
                            "Display Name: ${user.displayName ?: "Not set"}\n" +
                            "Email: ${user.email}\n" +
                            "Status: ${user.status}"
                        )
                        .setPositiveButton("OK", null)
                        .show()
                } else {
                    Toast.makeText(this@DashboardActivity, "Failed to load profile", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(this@DashboardActivity, "Error: ${e.message}", Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun showCreatePlanDialog() {
        val dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_create_plan, null)
        val titleInput = dialogView.findViewById<TextInputEditText>(R.id.plan_title_input)
        val descInput = dialogView.findViewById<TextInputEditText>(R.id.plan_description_input)

        MaterialAlertDialogBuilder(this)
            .setTitle("Create New Plan")
            .setView(dialogView)
            .setPositiveButton("Create") { _, _ ->
                val title = titleInput.text.toString()
                val description = descInput.text.toString()
                if (title.isNotEmpty()) {
                    createPlan(title, description)
                }
            }
            .setNegativeButton("Cancel", null)
            .show()
    }

    private fun createPlan(title: String, description: String) {
        lifecycleScope.launch {
            try {
                val request = CreatePlanRequest(
                    title = title,
                    description = description.ifEmpty { null },
                    startsAt = null,
                    endsAt = null,
                    capacity = null
                )
                val response = RetrofitClient.apiService.createPlan(request)
                if (response.isSuccessful) {
                    Toast.makeText(this@DashboardActivity, "Plan created!", Toast.LENGTH_SHORT).show()
                    loadPlans()
                } else {
                    Toast.makeText(this@DashboardActivity, "Failed to create plan", Toast.LENGTH_SHORT).show()
                }
            } catch (e: Exception) {
                Toast.makeText(this@DashboardActivity, "Error: ${e.message}", Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun performLogout() {
        lifecycleScope.launch {
            try {
                RetrofitClient.apiService.logout()
            } catch (e: Exception) {
                // Ignore logout errors
            }

            // Clear token
            getSharedPreferences("spontime", Context.MODE_PRIVATE)
                .edit()
                .remove("auth_token")
                .apply()

            RetrofitClient.setAuthToken(null)

            // Navigate to login
            startActivity(Intent(this@DashboardActivity, LoginActivity::class.java))
            finish()
        }
    }
}

class PlansAdapter : RecyclerView.Adapter<PlansAdapter.PlanViewHolder>() {

    private var plans: List<Plan> = emptyList()

    fun submitList(newPlans: List<Plan>) {
        plans = newPlans
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): PlanViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_plan, parent, false)
        return PlanViewHolder(view)
    }

    override fun onBindViewHolder(holder: PlanViewHolder, position: Int) {
        holder.bind(plans[position])
    }

    override fun getItemCount() = plans.size

    class PlanViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        private val titleText: TextView = itemView.findViewById(R.id.plan_title)
        private val descriptionText: TextView = itemView.findViewById(R.id.plan_description)
        private val hostText: TextView = itemView.findViewById(R.id.plan_host)

        fun bind(plan: Plan) {
            titleText.text = plan.title
            descriptionText.text = plan.description ?: "No description"
            hostText.text = "Host: ${plan.hostUser?.handle ?: "Unknown"}"
        }
    }
}
