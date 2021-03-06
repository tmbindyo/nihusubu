<?php

namespace App;

use App\Traits\UuidTrait;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class ManualJournal extends Model
{
    use SoftDeletes, UuidTrait;
    public $incrementing = false;

    // Parents
    public function status()
    {
        return $this->belongsTo('App\Status');
    }
    public function user()
    {
        return $this->belongsTo('App\User');
    }
    public function currency()
    {
        return $this->belongsTo('App\Currency');
    }
    public function institution()
    {
        return $this->belongsTo('App\Institution');
    }

    // Children
    public function manual_journal_accounts()
    {
        return $this->hasMany('App\ManualJournalAccount');
    }
}
