<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateTasksTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('tasks', function (Blueprint $table) {
            $table->uuid('id')->primary();

            $table->string('name', 200);
            $table->longText('description');
            $table->integer('priority');

            $table->date('start_date');
            $table->date('end_date');

            $table->integer('user_id')->unsigned();
            $table->integer('assignee_id')->unsigned();
            $table->uuid('status_id');
            $table->uuid('project_id');
            $table->uuid('milestone_id')->nullable();
            $table->uuid('task_list_id');

            $table->boolean('is_milestone');
            $table->boolean('is_task_list');
            $table->boolean('has_uploads');

            $table->timestamps();
            $table->softDeletes();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('tasks');
    }
}
